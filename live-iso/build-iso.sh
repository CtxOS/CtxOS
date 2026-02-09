#!/usr/bin/env bash
set -e

# Ensure we are in the script's directory
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Try to source logging helpers
if [ -f "../scripts/log.sh" ]; then
    source "../scripts/log.sh"
else
    log() { echo -e "\033[0;32m[INFO]\033[0m $1"; }
fi

# Requirement check: live-build
if ! command -v lb &> /dev/null; then
    echo "Error: live-build not found. Please install it first (apt install live-build)."
    exit 1
fi

# Prepare custom packages (like software-center)
chmod +x ./prepare-custom-packages.sh
./prepare-custom-packages.sh

lb clean
lb config \
  --distribution bookworm \
  --debian-installer live \
  --archive-areas "main contrib non-free non-free-firmware" \
  --architecture amd64 \
  --bootappend-live "boot=live components locales=en_US.UTF-8" \
  --binary-images iso-hybrid

# Copy local modules to chroot if needed
# mkdir -p config/includes.chroot/usr/local/bin
# cp ../scripts/*.sh config/includes.chroot/usr/local/bin/

log "Building ISO..."
lb build

# Profile-aware naming
ISO_NAME="ctxos-${PROFILE:-base}-$(date +%Y%m%d).iso"
if [ -f "live-image-amd64.hybrid.iso" ]; then
    log "Build successful. Renaming artifact to $ISO_NAME"
    mv live-image-amd64.hybrid.iso "$ISO_NAME"
fi
