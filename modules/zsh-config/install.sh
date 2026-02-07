#!/usr/bin/env bash
set -e
source ../../scripts/lib.sh

log "Installing zsh-config module"
if [ -s packages.txt ]; then
    xargs -a packages.txt apt-get install -y
fi

if [ -f "files/.zshrc" ]; then
    log "Installing .zshrc template"
    install_file "files/.zshrc" /etc/skel/.zshrc
    install_file "files/.zshrc" /root/.zshrc
fi
