#!/bin/bash

# CtxOS Container Images Build Script
# This script builds the official CtxOS container images in the correct order.

set -e

# Configuration
IMAGE_PREFIX="ctxos"
VERSION=$(cat ../VERSION 2>/dev/null || echo "latest")
CORE_TAG="${IMAGE_PREFIX}/core:${VERSION}"
SECURITY_TAG="${IMAGE_PREFIX}/security:${VERSION}"

echo "🚀 Starting CtxOS Container Images build..."

# 1. Build Core Image (Foundation)
echo "📦 Building Core Image: ${CORE_TAG}..."
docker build -t "${CORE_TAG}" -t "${IMAGE_PREFIX}/core:latest" ./core \
    --file ./core/Dockerfile \
    --build-arg CTXOS_VERSION="${VERSION}"

# 2. Build Security Image
echo "🛡️ Building Security Image: ${SECURITY_TAG}..."
# We use --build-context or just assume the previous build is in the local cache
docker build -t "${SECURITY_TAG}" -t "${IMAGE_PREFIX}/security:latest" ./security \
    --file ./security/Dockerfile \
    --build-arg CTXOS_VERSION="${VERSION}"

# 3. Build Tool & Category Images
echo "🛠️ Building Tool & Category Images..."

# Find all subdirectories in tools/
for TOOL_DIR in ./tools/*; do
    if [ -d "$TOOL_DIR" ]; then
        TOOL_NAME=$(basename "$TOOL_DIR")
        TOOL_TAG="${IMAGE_PREFIX}/tool-${TOOL_NAME}:${VERSION}"
        
        echo "   -> Building: ${TOOL_TAG}..."
        docker build -t "${TOOL_TAG}" -t "${IMAGE_PREFIX}/tool-${TOOL_NAME}:latest" "$TOOL_DIR" \
            --file "$TOOL_DIR/Dockerfile"
    fi
done

echo "✅ All CtxOS Container Images built successfully!"
echo "List of images:"
docker images | grep "${IMAGE_PREFIX}"
