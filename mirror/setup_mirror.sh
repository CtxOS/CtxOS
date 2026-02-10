#!/bin/bash
# -----------------------------------------------------------------------------
# CtxOS Mirror Setup Script
# Based on instructions: https://ctxos.github.io
# -----------------------------------------------------------------------------

set -e

# Configuration
MIRROR_DIR="/var/www/ctxos"
NGINX_CONF="/etc/nginx/sites-available/ctxos"
UPDATE_SCRIPT="/usr/local/bin/ctxos-mirror-update.sh"
DOMAIN="ctxos-mirror.example.com" # Change this or pass as argument
GPG_KEY_NAME="ctxOS Mirror"
GPG_KEY_EMAIL="repo@yourdomain.com"

# Check for root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root (sudo ./setup_mirror.sh)"
  exit 1
fi

# Detect OS
OS="$(uname -s)"
if [ "$OS" == "Darwin" ]; then
    echo "⚠️  Detected macOS. This script is intended for Debian/Linux servers."
    echo "    Some commands (apt-get, systemctl, user creation) will be skipped or simulated."
    MODE="macos"
    # Set dummy values for macOS testing
    MIRROR_USER=$(whoami)
    MIRROR_GROUP="staff"
else
    MODE="linux"
    MIRROR_USER="www-data"
    MIRROR_GROUP="www-data"
fi

echo "🚀 Starting CtxOS Mirror Setup..."

# 1. Create mirror directory
echo "📂 Creating mirror directory at $MIRROR_DIR..."
mkdir -p "$MIRROR_DIR"/pool
mkdir -p "$MIRROR_DIR"/dists

if [ "$MODE" == "linux" ]; then
    chown -R $MIRROR_USER:$MIRROR_GROUP "$MIRROR_DIR"
else
    echo "ℹ️  [macOS] Skipping chown (using current user)"
fi

# 2. Install necessary packages
echo "📦 Installing necessary packages..."
if [ "$MODE" == "linux" ]; then
    apt-get update
    apt-get install -y nginx dpkg-dev apt-utils wget gnupg
else
    echo "ℹ️  [macOS] Skipping apt-get install. Ensure you have 'wget', 'gpg', and 'nginx' installed manually."
fi

# 3. Create NGINX Configuration
echo "🌐 Configuring NGINX..."
# Only try to write to /etc/nginx if it exists or we are on Linux
if [ -d "/etc/nginx/sites-available" ]; then
    cat > "$NGINX_CONF" <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    root $MIRROR_DIR;
    autoindex on;

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF
    # Enable NGINX site
    ln -sf "$NGINX_CONF" /etc/nginx/sites-enabled/
    
    if command -v nginx >/dev/null; then
        if nginx -t; then
            if command -v systemctl >/dev/null; then
                systemctl reload nginx
            elif command -v service >/dev/null; then
                service nginx reload
            else
                echo "⚠️  Could not reload NGINX (systemctl/service not found)"
            fi
            echo "✅ NGINX configured and reloaded."
        else
            echo "❌ NGINX configuration failed."
        fi
    else
        echo "⚠️  NGINX not found. Skipping reload."
    fi
else
    echo "ℹ️  [macOS/Other] /etc/nginx/sites-available not found. Skipping NGINX config write."
    echo "    Sample config would be:"
    echo "    root $MIRROR_DIR;"
    echo "    autoindex on;"
fi

# 4. GPG Key Generation (Interactive)
echo "🔐 GPG Key Generation"
echo "You need a GPG key to sign the repository."
echo "Checking existing keys..."
gpg --list-keys

read -p "Do you want to generate a NEW GPG key now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Generating GPG key..."
    gpg --full-generate-key
fi

echo "⚠️  IMPORTANT: Please note your GPG Key ID for the update script configuration."

# 5. Install Update Script
echo "📜 Installing auto-update script to $UPDATE_SCRIPT..."
cp update_mirror.sh "$UPDATE_SCRIPT"
chmod +x "$UPDATE_SCRIPT"

# 6. Final Instructions
echo ""
echo "✅ Setup Complete! Next steps:"
echo "1. Edit $UPDATE_SCRIPT and set your GPG_KEY_ID."
echo "2. Run 'certbot --nginx -d $DOMAIN' to enable HTTPS."
echo "3. Run '$UPDATE_SCRIPT' to perform the initial sync and signing."
echo "4. Add a cron job to keep it updated:"
echo "   0 3 * * * $UPDATE_SCRIPT"
