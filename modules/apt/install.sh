#!/usr/bin/env bash
set -e
source ../../scripts/lib.sh

log "Installing apt module"
if [ -s packages.txt ]; then
    xargs -a packages.txt apt-get install -y
fi

# Skip repo setup in rescue profile
if [ "${PROFILE:-base}" != "rescue" ]; then
    log "Configuring CtxOS repository"
    if [ -f "files/keyrings/ctxos.gpg" ]; then
        install_file "files/keyrings/ctxos.gpg" /usr/share/keyrings/ctxos.gpg
    fi
    if [ -f "files/ctxos.list" ]; then
        install_file "files/ctxos.list" /etc/apt/sources.list.d/ctxos.list
    fi
    log "Updating package lists (this may fail if the repository is not yet live)..."
    # We use || true because the repository might not be published yet on first install
    apt-get update -o Acquire::Retries=1 -o Acquire::http::Timeout="5" || warn "Some repositories could not be updated. This is expected if the CtxOS repo is not yet live."
fi

