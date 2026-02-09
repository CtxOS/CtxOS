#!/usr/bin/env bash
# remote-install.sh - One-line installer for users
set -e

# --- Configuration (User should update these) ---
REPO_DOMAIN="ctxos.github.io"
KEY_URL="https://${REPO_DOMAIN}/ctxos.asc"
REPO_URL="https://${REPO_DOMAIN}"
DISTRO="bookworm"
COMPONENT="main"
# ------------------------------------------------

log() { echo -e "\033[0;32m[INSTALL]\033[0m $1"; }

if [[ $EUID -ne 0 ]]; then
   echo "Please run as root (sudo)"
   exit 1
fi

check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: Required command not found: $1"
        exit 1
    fi
}

check_command "curl"
check_command "gpg"

log "Downloading distribution GPG key..."
curl -fsSL "$KEY_URL" | gpg --dearmor -o /usr/share/keyrings/ctxos.gpg

log "Adding repository to sources..."
echo "deb [signed-by=/usr/share/keyrings/ctxos.gpg] $REPO_URL $DISTRO $COMPONENT" \
    > /etc/apt/sources.list.d/ctxos.list

log "Updating package lists..."
apt-get update

log "✅ CtxOS repository is now active."
log "You can now run: apt install ctxos-core"
