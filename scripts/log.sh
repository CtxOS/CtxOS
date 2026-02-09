#!/usr/bin/env bash
# log.sh - Logging utilities for ctxos

COLOR_GREEN='\033[0;32m'
COLOR_BLUE='\033[0;34m'
COLOR_RED='\033[0;31m'
COLOR_CYAN='\033[0;36m'
COLOR_RESET='\033[0m'

log() {
    echo -e "${COLOR_GREEN}[INFO]${COLOR_RESET} $1"
}

warn() {
    echo -e "${COLOR_BLUE}[WARN]${COLOR_RESET} $1"
}

error() {
    echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1"
}
