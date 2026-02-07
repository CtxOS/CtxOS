#!/usr/bin/env bash
set -e
source ../../scripts/lib.sh

log "Installing layout-switcher module"
if [ -s packages.txt ]; then
    xargs -a packages.txt apt-get install -y
fi

if [ -d "files" ] && [ "$(ls -A files)" ]; then
    log "Installing files for layout-switcher"
    # Add custom installation logic here
fi
