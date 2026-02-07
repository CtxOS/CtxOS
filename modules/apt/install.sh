#!/usr/bin/env bash
set -e
source ../../scripts/lib.sh

log "Installing apt module"
if [ -s packages.txt ]; then
    xargs -a packages.txt apt-get install -y
fi

# Skip repo setup in rescue profile
if [ "${PROFILE:-base}" != "rescue" ]; then
    log "Configuring Debian Base Kit repository"
    if [ -f "files/keyrings/debian-base-kit.gpg" ]; then
        install_file "files/keyrings/debian-base-kit.gpg" /usr/share/keyrings/debian-base-kit.gpg
    fi
    if [ -f "files/debian-base-kit.list" ]; then
        install_file "files/debian-base-kit.list" /etc/apt/sources.list.d/debian-base-kit.list
    fi
    apt-get update
fi

