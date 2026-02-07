#!/usr/bin/env bash
set -e
source ../../scripts/lib.sh

log "Installing core packages"
apt-get update
xargs -a packages.txt apt-get install -y

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
