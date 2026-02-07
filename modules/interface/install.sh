#!/usr/bin/env bash
set -e
source ../../scripts/lib.sh

log "Installing interface module"
if [ -s packages.txt ]; then
    xargs -a packages.txt apt-get install -y
fi

if [ -d "files" ] && [ "$(ls -A files)" ]; then
    log "Installing files for interface"
    # Add custom installation logic here
fi
