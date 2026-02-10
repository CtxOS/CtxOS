#!/bin/bash
# -----------------------------------------------------------------------------
# CtxOS Mirror Auto-Update Script
# mirrors requested site, rebuilds metadata, and signs it.
# -----------------------------------------------------------------------------

set -e

# Configuration - EDIT THIS
GPG_KEY_ID="ABCD1234EF567890" # Replace with your GPG Key ID
MIRROR_DIR="/var/www/ctxos"
SOURCE_URL="https://ctxos.github.io/"

# Ensure we are root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root"
  exit 1
fi

echo "🔄 Starting Mirror Update..."
cd "$MIRROR_DIR"

# 1. Mirror content
echo "📥 Downloading updates from $SOURCE_URL..."
wget -r -np -nH --cut-dirs=0 \
     --reject "index.html*" \
     "$SOURCE_URL" -N

# 2. Rebuild Metadata
echo "📦 Rebuilding repository metadata..."

# Generate Packages file from pool/ directory
if [ -d "pool" ]; then
    dpkg-scanpackages pool /dev/null > Packages
    gzip -kf Packages
else
    echo "⚠️  Warning: 'pool' directory not found. Skipping package scan."
fi

# Generate Release file
apt-ftparchive release . > Release

# 3. Sign Release
echo "✍️  Signing Release file with GPG Key: $GPG_KEY_ID..."
gpg --default-key "$GPG_KEY_ID" --batch --yes --clearsign -o InRelease Release
gpg --default-key "$GPG_KEY_ID" --batch --yes -abs -o Release.gpg Release

# 4. Fix Permissions
if [ "$(uname -s)" == "Darwin" ]; then
    echo "ℹ️  [macOS] Skipping chown (permissions ok)"
else
    echo "pcl Fixing permissions..."
    chown -R www-data:www-data "$MIRROR_DIR"
fi

echo "✅ Mirror Update Complete."
