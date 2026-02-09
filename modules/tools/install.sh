#!/usr/bin/env bash
set -e
source ../../scripts/lib.sh

log "Installing tools module"
if [ -s packages.txt ]; then
    while read -r pkg; do
        [ -z "$pkg" ] && continue
        log "  + $pkg"
        apt-get install -y "$pkg" || warn "Failed to install $pkg (skipping)"
    done < packages.txt
fi

if [ -d "files" ] && [ "$(ls -A files)" ]; then
    log "Installing files for tools"
    # Add custom installation logic here
fi
