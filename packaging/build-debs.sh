#!/usr/bin/env bash
set -e
SCRIPTS_DIR="$(dirname "${BASH_SOURCE[0]}")/../scripts"
source "$SCRIPTS_DIR/log.sh"

# Check dependencies
if ! command -v dpkg-deb &> /dev/null; then
    error "dpkg-deb not found. Install 'dpkg' (e.g., brew install dpkg) or run in Docker."
    exit 1
fi

# Base packaging directory
BASE_DIR="$(dirname "${BASH_SOURCE[0]}")"
DEB_DIR="$BASE_DIR/deb"
BUILD_DIR="$BASE_DIR/../build/debs"

# Read current version
VERSION=$(cat "$BASE_DIR/../VERSION" || echo "1.0.1")

PACKAGES=(
    "ctxos-core" 
    "ctxos-configs-zsh"
    "0trace"
    "ctxos-menu"    "debian-base-desktop" 
    "debian-base-tools"
    "ctxos-tools-web"
    "ctxos-tools-wireless"
    "ctxos-tools-forensics"
    "ctxos-tools-reversing"
    "ctxos-tools-automotive"
    "ctxos-tools"
)

mkdir -p "$BUILD_DIR"

# 1. Build Meta-packages from packaging/deb
for pkg in "${PACKAGES[@]}"; do
    PKG_PATH="$DEB_DIR/$pkg"
    log "▶ Building $pkg..."
    
    if [ -d "$PKG_PATH" ]; then
        if [ -f "$PKG_PATH/debian/control" ]; then
            log "  Building standard Debian package $pkg ($VERSION)..."
            # Note: For meta-packages we can often use dpkg-deb --build if they are simple directories,
            # but since we have debian/ folders, we use dpkg-buildpackage
            (
                cd -P "$PKG_PATH" && \
                dpkg-buildpackage -us -uc -b && \
                mv ../"${pkg}"_*.deb "$BUILD_DIR/" 2>/dev/null && \
                rm -f ../"${pkg}"_*.{buildinfo,changes}
            ) || warn "Build failed for $pkg"
        else
            warn "No control file for $pkg, skipping."
        fi
    else
        warn "Directory $PKG_PATH not found."
    fi
done

# 2. Build Software Center
log "▶ Building software-center..."
if [ -d "$BASE_DIR/../software-center" ]; then
    (
        cd "$BASE_DIR/../software-center" && \
        dpkg-buildpackage -us -uc -b && \
        mv ../software-center_*.deb "$BUILD_DIR/" 2>/dev/null && \
        rm -f ../software-center_*.{buildinfo,changes}
    ) || warn "Build failed for software-center"
fi

echo "Done! Packages are in build/debs/"
