#!/usr/bin/env bash
# pipeline-master.sh - The high-level orchestrator for the entire distribution lifecycle
set -e

log() { echo -e "\033[0;35m[PIPELINE]\033[0m $1"; }

# 0. Sync Upstream Mirrors
log "Stage 0: Synchronizing Upstream Mirrors..."
if [ "$SKIP_MIRROR" != "true" ]; then
    ./scripts/mirror-sync.sh all
fi

# 1. Bump version and build packages (Core)
log "Stage 1: Building Core Packages & Versioning..."
./scripts/release.sh "${1:-patch}"

# 1.5 Build Registered Projects
log "Stage 1.5: Skipping Registered Projects (sample-app)..."
# ./scripts/project-packager.sh build "sample-app"

# 2. Build Docker Image
log "Stage 2: Building Distribution Docker Image..."
docker build -t ctxos-base:latest .

# 2.5 Generate System Metadata
log "Stage 2.5: Generating Distribution Metadata..."
./scripts/generate-metadata.sh

# 3. Build Live ISO
log "Stage 3: Building Live ISO (x86_64)..."
if [ "$SKIP_ISO" != "true" ]; then
    cd live-iso
    ./build-iso.sh
    cd ..
else
    log "Skipping ISO build as requested."
fi

# 3.5 Build Multi-Arch Images (Optional)
log "Stage 3.5: Building Multi-Arch Images (ARM/RISC-V)..."
if [ "$BUILD_MULTI_ARCH" == "true" ]; then
    sudo ./live-iso/armbian-builder/build-image.sh aarch64 ubuntu
else
    log "Skipping Multi-Arch build. Set BUILD_MULTI_ARCH=true to enable."
fi

# 3.8 Update APT Repository
log "Stage 3.8: Updating APT Repository..."
# Ensure debs from build_output are in incoming
mkdir -p packaging/repo/incoming
find build_output/ -name "*.deb" -exec cp {} packaging/repo/incoming/ \;
./packaging/repo/manage-repo.sh add
./packaging/repo/manage-repo.sh publish
./packaging/repo/manage-repo.sh sync-web

# 4. Validate everything
log "Stage 4: Artifact Validation & Release Notes..."
./scripts/validate-artifacts.sh
./scripts/generate-release-notes.sh

# 4.5 Security Audit
log "Stage 4.5: Running Security Audit..."
./scripts/security-audit.sh

# 5. Summary
VERSION=$(cat VERSION)
log "✅ Pipeline Complete for v$VERSION"
log "Artifacts ready:"
echo " - Packages: build_output/"
echo " - Docker: ctxos-base:latest"
echo " - ISO: $(find . -maxdepth 1 -name "*.iso" -print0 | xargs -0 ls -t | head -n 1)"
echo " - Repo: packaging/repo/ (Aptly published)"
