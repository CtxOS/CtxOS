#!/usr/bin/env bash
# run-pipeline.sh - Run the CtxOS pipeline in a self-contained container
set -e

DIR="$(pwd)"
IMAGE_NAME="ctxos-builder-full"

echo "🛠️ Building self-contained build environment (copying source)..."
# We create a temporary Dockerfile that includes the COPY step
cat <<EOF > Dockerfile.full
FROM ctxos-builder
COPY . /app
WORKDIR /app
EOF

# Ensure base image exists first
docker build -t ctxos-builder -f "$DIR/Dockerfile.build" .

docker build -t $IMAGE_NAME -f Dockerfile.full .
rm Dockerfile.full

echo "🚀 Starting CtxOS Pipeline inside container..."
# Run the container and name it so we can copy artifacts out
CONTAINER_NAME="ctxos-build-run-$(date +%s)"

# Run privileged for live-build (mounting loop devices)
docker run --name "$CONTAINER_NAME" \
    --privileged \
    -e SKIP_SIGNING=true \
    $IMAGE_NAME ./scripts/pipeline-master.sh "$1"

echo "📥 Copying artifacts and metadata back to host..."
mkdir -p build_output
docker cp "$CONTAINER_NAME":/app/build_output/. ./build_output/ || true
docker cp "$CONTAINER_NAME":/app/*.iso ./ || true
docker cp "$CONTAINER_NAME":/app/VERSION ./VERSION || true

# Copy changelogs back for version sync
for mod in software-center packaging/deb/debian-base-core packaging/deb/debian-base-desktop packaging/deb/debian-base-tools packaging/deb/ctxos-tools-web packaging/deb/ctxos-tools-wireless packaging/deb/ctxos-tools-forensics packaging/deb/ctxos-tools-reversing packaging/deb/ctxos-tools-automotive packaging/deb/ctxos-tools; do
    docker cp "$CONTAINER_NAME":/app/"$mod"/debian/changelog ./"$mod"/debian/changelog || true
done

echo "🧹 Cleaning up container..."
docker rm "$CONTAINER_NAME"

echo "✅ Done! Check build_output/ and current directory for ISOs."
