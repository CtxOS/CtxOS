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

PACKAGES=("debian-base-core" "debian-base-desktop" "debian-base-tools")

mkdir -p "$BUILD_DIR"

for pkg in "${PACKAGES[@]}"; do
    PKG_PATH="$DEB_DIR/$pkg"
    log "▶ Building $pkg..."
    
    if [ -d "$PKG_PATH" ]; then
        # Ensure DEBIAN/control exists
        if [ ! -f "$PKG_PATH/DEBIAN/control" ]; then
            warn "No control file for $pkg, skipping."
            continue
        fi
        
        # Ensure correct permissions for maintenance scripts
        if [ -f "$PKG_PATH/DEBIAN/postinst" ]; then
            chmod 755 "$PKG_PATH/DEBIAN/postinst"
        fi
        
        # Build the package
        dpkg-deb --build "$PKG_PATH" "$BUILD_DIR/${pkg}_1.0.0_all.deb"
    else
        warn "Directory $PKG_PATH not found."
    fi
done

echo "Done! Packages are in build/debs/"
