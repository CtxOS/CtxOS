#!/usr/bin/env bash
set -e
source ../../scripts/lib.sh

log "Installing core packages"
# Update is handled by apt module, but we do a quick refresh if needed
apt-get update -o Acquire::Retries=1 -o Acquire::http::Timeout="5" || warn "Standard repository update failed. Continuing anyway..."
if [ -s packages.txt ]; then
    while read -r pkg; do
        [ -z "$pkg" ] && continue
        log "  + $pkg"
        apt-get install -y "$pkg" || warn "Failed to install $pkg (skipping)"
    done < packages.txt
fi

if [ -d "files" ]; then
    for f in files/*; do
        if [ -f "$f" ]; then
            case $(basename "$f") in
                sysctl.conf)
                    install_file "$f" /etc/sysctl.d/99-core.conf
                    ;;
                limits.conf)
                    install_file "$f" /etc/security/limits.d/99-core.conf
                    ;;
            esac
        fi
    done
fi
