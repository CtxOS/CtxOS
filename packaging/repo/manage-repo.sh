#!/usr/bin/env bash
# manage-repo.sh - Automate Debian Base Kit APT Repo management
set -e

REPO_NAME="debian-base-kit"
DISTRIBUTION="bookworm"
COMPONENT="main"
GPG_KEY="Debian Base Kit"
ROOT_DIR="/var/lib/aptly"
INCOMING_DIR="$ROOT_DIR/incoming"

log() { echo -e "\033[0;32m[REPO]\033[0m $1"; }

usage() {
    echo "Usage: $0 {init|add|publish|cleanup}"
    exit 1
}

case "$1" in
    init)
        log "Initializing aptly repo..."
        aptly repo create -distribution="$DISTRIBUTION" -component="$COMPONENT" "$REPO_NAME"
        ;;
    add)
        log "Adding packages from $INCOMING_DIR..."
        aptly repo add "$REPO_NAME" "$INCOMING_DIR"
        ;;
    publish)
        VERSION=$(date +%Y%m%d%H%M)
        SNAPSHOT_NAME="${REPO_NAME}-${VERSION}"
        log "Creating snapshot $SNAPSHOT_NAME..."
        aptly snapshot create "$SNAPSHOT_NAME" from repo "$REPO_NAME"
        
        log "Publishing snapshot..."
        if aptly publish list | grep -q "$REPO_NAME"; then
            aptly publish switch "$DISTRIBUTION" "$SNAPSHOT_NAME"
        else
            aptly publish snapshot -gpg-key="$GPG_KEY" -distribution="$DISTRIBUTION" "$SNAPSHOT_NAME"
        fi
        ;;
    cleanup)
        log "Cleaning up old snapshots..."
        aptly snapshot list -raw | grep "${REPO_NAME}-" | head -n -3 | xargs -r -n 1 aptly snapshot drop
        ;;
    *)
        usage
        ;;
esac
