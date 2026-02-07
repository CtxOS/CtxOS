#!/usr/bin/env bash
# build-image.sh - The Multi-Arch Image Builder for CtxOS
set -e

ARCH=${1:-"aarch64"}
DISTRO=${2:-"ubuntu"}
VERSION=$(cat VERSION 2>/dev/null || echo "1.0.0")
TARGET_DIR="build/images/$ARCH/$VERSION"

# Visual Helpers
C_BLUE="\033[0;34m"
C_CYAN="\033[0;36m"
C_GREEN="\033[0;32m"
C_RESET="\033[0m"

log() { echo -e "${C_BLUE}[BUILDER]${C_RESET} ${C_GREEN}$1${C_RESET}"; }
error() { echo -e "${C_CYAN}[ERROR]${C_RESET} ${C_BLUE}$1${C_RESET}"; exit 1; }

# 1. Verification
log "Starting build for $DISTRO ($ARCH)..."
if [[ "$EUID" -ne 0 ]]; then
   error "Please run as root (required for chroot and mounts)."
fi

# 2. Dependency Check
log "Checking host dependencies..."
deps=("qemu-user-static" "binfmt-support" "debootstrap" "rsync" "parted")
for dep in "${deps[@]}"; do
    if ! command -v "$dep" &> /dev/null; then
        log "Warning: $dep not found. Attempting to install..."
        apt-get update && apt-get install -y "$dep"
    fi
done

# 3. Prepare Workspace
mkdir -p "$TARGET_DIR"
ROOTFS_DIR="$TARGET_DIR/rootfs"
mkdir -p "$ROOTFS_DIR"

# 4. Bootstrap Rootfs
log "Bootstrapping $DISTRO rootfs for $ARCH..."
if [ "$DISTRO" == "ubuntu" ]; then
    debootstrap --arch="$ARCH" --foreign jammy "$ROOTFS_DIR" http://ports.ubuntu.com/
elif [ "$DISTRO" == "debian" ]; then
    debootstrap --arch="$ARCH" --foreign bookworm "$ROOTFS_DIR" http://deb.debian.org/debian/
fi

# 5. QEMU Setup for Cross-Arch
log "Setting up QEMU for $ARCH..."
cp /usr/bin/qemu-"$ARCH"-static "$ROOTFS_DIR/usr/bin/"

# 6. First Stage Chroot (Finish Bootstrap)
log "Completing second-stage bootstrap..."
chroot "$ROOTFS_DIR" /debootstrap/debootstrap --second-stage

# 7. Mount pseudo-filesystems
log "Mounting pseudo-filesystems..."
mkdir -p "$ROOTFS_DIR/proc" "$ROOTFS_DIR/sys" "$ROOTFS_DIR/dev"
mount -t proc none "$ROOTFS_DIR/proc"
mount -t sysfs none "$ROOTFS_DIR/sys"
mount -o bind /dev "$ROOTFS_DIR/dev"
mount -o bind /dev/pts "$ROOTFS_DIR/dev/pts"

# 8. Customize Rootfs
log "Running customization scripts..."
mkdir -p "$ROOTFS_DIR/tmp/dbk-build"
cp /Users/khulnasoft/debian-dev-kit/software-center/build_output/*.deb "$ROOTFS_DIR/tmp/dbk-build/" || log "Warning: No .deb files found"
cp /Users/khulnasoft/debian-dev-kit/live-iso/armbian-builder/scripts/customize-rootfs.sh "$ROOTFS_DIR/tmp/dbk-build/"

chroot "$ROOTFS_DIR" /bin/bash /tmp/dbk-build/customize-rootfs.sh

# Cleanup mounts
umount "$ROOTFS_DIR/proc"
umount "$ROOTFS_DIR/sys"
umount "$ROOTFS_DIR/dev/pts"
umount "$ROOTFS_DIR/dev"

# 9. Cleanup & Image Creation
log "Generating bootable image..."
# (Integration with setup-bootloader.sh and image assembly goes here)

log "✅ Build complete for $ARCH"
