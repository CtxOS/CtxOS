#!/usr/bin/env bash
# manage-repo.sh - Automate CtxOS APT Repo management
set -e

REPO_NAME="ctxos"
DISTRIBUTION="bookworm"
COMPONENT="main"
GPG_KEY="CtxOS"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INCOMING_DIR="$ROOT_DIR/incoming"
mkdir -p "$INCOMING_DIR"

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
        log "Checking if repo $REPO_NAME exists..."
        if ! aptly repo show "$REPO_NAME" &> /dev/null; then
            log "Repo not found, initializing..."
            aptly repo create -distribution="$DISTRIBUTION" -component="$COMPONENT" "$REPO_NAME"
        fi
        log "Adding packages from $INCOMING_DIR..."
        aptly repo add "$REPO_NAME" "$INCOMING_DIR"
        ;;
    publish)
        VERSION=$(date +%Y%m%d%H%M)
        SNAPSHOT_NAME="${REPO_NAME}-${VERSION}"
        log "Creating snapshot $SNAPSHOT_NAME..."
        aptly snapshot create "$SNAPSHOT_NAME" from repo "$REPO_NAME"
        
        log "Publishing snapshot..."
        SIGN_FLAGS="-gpg-key=$GPG_KEY"
        if [ "$SKIP_SIGNING" == "true" ]; then
            SIGN_FLAGS="-skip-signing"
        fi

        if aptly publish list | grep -q "$REPO_NAME"; then
            aptly publish switch $SIGN_FLAGS "$DISTRIBUTION" "$SNAPSHOT_NAME"
        else
            aptly publish snapshot $SIGN_FLAGS \
                -architectures="amd64,arm64,all" \
                -distribution="$DISTRIBUTION" "$SNAPSHOT_NAME"
        fi
        ;;
    cleanup)
        log "Cleaning up old snapshots..."
        aptly snapshot list -raw | grep "${REPO_NAME}-" | head -n -3 | xargs -r -n 1 aptly snapshot drop
        ;;
    sync-web)
        log "Syncing published repo to web directory..."
        # Aptly publishes to ~/.aptly/public by default if rootDir isn't absolute in certain contexts,
        # but here rootDir is /var/lib/aptly.
        # We'll copy the contents to a local 'repo' folder for GitHub Pages.
        mkdir -p ../../repo
        cp -rv /var/lib/aptly/public/* ../../repo/
        ;;
    *)
        usage
        ;;
esac
