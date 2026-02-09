#!/usr/bin/env bash
# release.sh - Orchestrate system-wide releases for CtxOS
set -e

# Configuration
VERSION_FILE="VERSION"
REPO_DIR="packaging/repo"
MODULES=("software-center" "packaging/deb/debian-base-core" "packaging/deb/debian-base-desktop" "packaging/deb/debian-base-tools")

log() { echo -e "\033[0;34m[RELEASE]\033[0m $1"; }
error() { echo -e "\033[0;31m[ERROR]\033[0m $1"; exit 1; }

usage() {
    echo "Usage: $0 {patch|minor|major|status}"
    echo "Example: $0 patch"
    exit 1
}

if [ ! -f "$VERSION_FILE" ]; then
    echo "1.0.0" > "$VERSION_FILE"
fi

CURRENT_VERSION=$(cat "$VERSION_FILE")

case "$1" in
    status)
        log "Current System Version: $CURRENT_VERSION"
        exit 0
        ;;
    patch|minor|major)
        # Calculate new version
        IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"
        case "$1" in
            patch) patch=$((patch + 1)) ;;
            minor) minor=$((minor + 1)); patch=0 ;;
            major) major=$((major + 1)); minor=0; patch=0 ;;
        esac
        NEW_VERSION="${major}.${minor}.${patch}"
        ;;
    *)
        usage
        ;;
esac

log "Bumping version: $CURRENT_VERSION -> $NEW_VERSION"

# 1. Update Version File
echo "$NEW_VERSION" > "$VERSION_FILE"

# 1.1 Sync Frontend Version
if [ -f "workflow/package.json" ]; then
    log "Syncing workflow/package.json version..."
    sed -i.bak "s/\"version\": \".*\"/\"version\": \"$NEW_VERSION\"/" workflow/package.json && rm workflow/package.json.bak
fi

# 2. Update Debian Changelogs for all modules
for mod in "${MODULES[@]}"; do
    if [ -d "$mod/debian" ]; then
        log "Updating changelog for $mod..."
        # Using dch (debian changelog tool) if available, or simple append
        if command -v dch &> /dev/null; then
            (cd "$mod" && dch -v "$NEW_VERSION" "Release $NEW_VERSION")
        else
            # Simple fallback for development
            DATE=$(date -R)
            cat <<EOF > "$mod/debian/changelog.new"
$(basename "$mod") ($NEW_VERSION) unstable; urgency=low

  * Automated release bump to $NEW_VERSION

 -- Debian Base Kit Team <team@debianbasekit.org>  $DATE

$(cat "$mod/debian/changelog")
EOF
            mv "$mod/debian/changelog.new" "$mod/debian/changelog"
        fi
    fi
done

# 3. Build Packages
log "Building all modules..."
mkdir -p build_output
for mod in "${MODULES[@]}"; do
    log "Building $mod..."
    if [ -f "$mod/Makefile" ]; then
        (cd "$mod" && make build-deb DESTDIR=../../build_output) || log "Warning: Build failed for $mod"
    elif [ -d "$mod/debian" ]; then
        (cd "$mod" && debuild -us -uc -b) || log "Warning: Build failed for $mod"
    fi
done

# 4. Integrate with Repository
log "Pushing packages to local repository..."
# Assuming artifacts are in the parent of the modules as per debuild
find . -name "*.deb" -exec cp {} "$REPO_DIR/incoming/" \;

log "Updating Aptly Repository..."
./$REPO_DIR/manage-repo.sh add
./$REPO_DIR/manage-repo.sh publish

# 5. Git Tagging
if [ -d ".git" ]; then
    log "Creating git tag v$NEW_VERSION..."
    git add "$VERSION_FILE"
    for mod in "${MODULES[@]}"; do git add "$mod/debian/changelog"; done
    git commit -m "chore: release v$NEW_VERSION" || true
    git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"
fi

log "✅ Success! Version $NEW_VERSION is now published to the Aptly repository."
