#!/usr/bin/env bash
# project-packager.sh - Orchestrate builds for any project in the registry
set -e

MANIFEST="projects/manifest.yaml"
ARCHIVE_ROOT="archive"
REPO_MANAGER="packaging/repo/manage-repo.sh"

log() { echo -e "\033[0;32m[PACKAGER]\033[0m $1"; }
error() { echo -e "\033[0;31m[ERROR]\033[0m $1"; exit 1; }

build_project() {
    local name=$1
    log "Processing project: $name"
    
    # In a real tool, we'd use yq to parse the yaml
    # For this prototype, we'll grep the path
    local path
    path=$(grep -A 3 "name: \"$name\"" "$MANIFEST" | grep "path:" | cut -d'"' -f2)
    
    if [ ! -d "$path" ]; then
        error "Project path $path not found for $name"
    fi

    log "Building $name at $path..."
    (cd "$path" && if [ -f Makefile ]; then make build-deb; else debuild -us -uc -b; fi)

    # Move to Archive Store
    log "Archiving artifacts..."
    find "$path/.." -maxdepth 1 -name "*.deb" -exec cp {} "$ARCHIVE_ROOT/amd64/" \;
}

publish_to_repo() {
    log "Publishing archived packages to Aptly..."
    # Assuming manage-repo.sh handles the sync from incoming/
    cp archive/amd64/*.deb packaging/repo/incoming/
    ./$REPO_MANAGER add
    ./$REPO_MANAGER publish
}

case "$1" in
    "build")
        if [ -n "$2" ]; then
            build_project "$2"
        else
            echo "Usage: $0 build <project-name>"
        fi
        ;;
    "publish")
        publish_to_repo
        ;;
    *)
        echo "Usage: $0 {build|publish}"
        exit 1
        ;;
esac
