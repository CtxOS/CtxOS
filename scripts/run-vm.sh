#!/usr/bin/env bash
# run-vm.sh - Launch the CtxOS ISO in a QEMU Virtual Machine
set -e

ISO_FILE=$1
MEM="2G"
CPUS="2"

log() { echo -e "\033[0;35m[VM-LAUNCH]\033[0m $1"; }

if [ -z "$ISO_FILE" ]; then
    # Try to find the latest ISO
    ISO_FILE=$(find . -maxdepth 1 -name "*.iso" -print0 | xargs -0 ls -t | head -n 1)
fi

if [ ! -f "$ISO_FILE" ]; then
    echo "Error: No ISO file found. Build one first using live-iso/build-iso.sh"
    exit 1
fi

# Check for QEMU
if ! command -v qemu-system-x86_64 &> /dev/null; then
    echo "Error: qemu-system-x86_64 not found. Please install qemu-system-x86."
    exit 1
fi

log "Launching VM with $ISO_FILE..."
log "Resources: $CPUS CPUs, $MEM RAM"

qemu-system-x86_64 \
    -enable-kvm \
    -m $MEM \
    -smp $CPUS \
    -drive file="$ISO_FILE",format=raw,if=virtio,readonly=on \
    -net nic,model=virtio -net user \
    -vga virtio \
    -display gtk,gl=on \
    -cpu host \
    -usb -device usb-tablet
