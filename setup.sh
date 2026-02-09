#!/usr/bin/env bash
set -e
source scripts/require-root.sh
source scripts/log.sh

PROFILE="${1:-base}"
PROFILE_FILE="profiles/$PROFILE.mk"

# Check required commands
check_command() {
    if ! command -v "$1" &> /dev/null; then
        error "Required command not found: $1"
        exit 1
    fi
}

check_command "dpkg"
check_command "apt-get"

if [ ! -f "$PROFILE_FILE" ]; then
    error "Unknown profile: $PROFILE"
    exit 1
fi

log "Starting Debian Base Kit Installation (Profile: $PROFILE)"

# Ensure all installer scripts are executable
chmod +x scripts/*.sh
chmod +x modules/*/install.sh 2>/dev/null || true
chmod +x modules/*/remove.sh 2>/dev/null || true

# Load profile
# shellcheck disable=SC1090
source "$PROFILE_FILE"

for m in ${MODULES}; do
  if [ -d "modules/$m" ] && [ -f "modules/$m/install.sh" ]; then
    log "▶ Installing module: $m"
    (cd "modules/$m" && bash ./install.sh)
  else
    warn "Module $m not found or missing install.sh"
  fi
done

log "Installation complete!"
