#!/usr/bin/env bash
# docker-run.sh - Run the CtxOS toolkit inside Docker
set -e

IMAGE_NAME="ctxos-base-kit"
CONTAINER_NAME="ctxos-toolkit"

log() { echo -e "\033[0;34m[DOCKER]\033[0m $1"; }

# 1. Build the image if it doesn't exist or --build is passed
if [[ "$1" == "--build" ]] || [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
    log "Building Docker image $IMAGE_NAME..."
    docker build -t $IMAGE_NAME .
fi

# 2. Handle GUI support (X11 forwarding)
X11_OPTS=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    X11_OPTS="-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix"
    xhost +local:docker &> /dev/null || true
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # For macOS, XQuartz is required. This is a best-effort configuration.
    IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
    X11_OPTS="-e DISPLAY=$IP:0"
    if [ -n "$IP" ]; then
        xhost + "$IP" &> /dev/null || true
    fi
fi

# 3. Run the container
log "Starting toolkit container..."
docker run -it --rm \
    --name $CONTAINER_NAME \
    --privileged \
    "$X11_OPTS" \
    -v "$(pwd):/app" \
    $IMAGE_NAME /bin/bash
