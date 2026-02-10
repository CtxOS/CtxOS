# 🪞 CtxOS Mirror Setup (Production Ready)

This directory contains scripts and documentation to set up a fully functional, GPG-signed APT repository mirror for CtxOS. This setup is ideal for isolated environments (SOC, Labs), offline deployments, or simply reducing upstream bandwidth usage.

## 🚀 One-Click Setup (Almost)

We provide a `setup_mirror.sh` script to automate most of the configuration.

1.  **Edit Configuration**: Open `setup_mirror.sh` and set your `DOMAIN`, `GPG_KEY_EMAIL`, and other variables.
2.  **Run Setup**:
    ```bash
    sudo ./setup_mirror.sh
    ```
    This will:
    *   Create the mirror directory structure (`/var/www/ctxos`).
    *   Install required packages (`nginx`, `dpkg-dev`, `apt-utils`, etc.).
    *   Configure NGINX for HTTP (Port 80).
    *   Guide you through generating a GPG signing key.
    *   Install the auto-update script to `/usr/local/bin/ctxos-mirror-update.sh`.

## 🔐 Post-Setup Tasks (Required)

### 1. Enable HTTPS
Secure your mirror with Let's Encrypt (highly recommended):
```bash
sudo certbot --nginx -d ctxos-mirror.example.com
```

### 2. Configure GPG Key ID
After generating your GPG key, you must add its Key ID to the update script.

1.  List keys to find your ID:
    ```bash
    gpg --list-keys
    # Look for the line starting with 'pub', e.g., 'ABCD1234EF567890'
    ```
2.  Edit the update script:
    ```bash
    sudo nano /usr/local/bin/ctxos-mirror-update.sh
    ```
3.  Update the `GPG_KEY_ID` variable with your key ID.

### 3. Initial Sync
Run the update script manually to perform the first sync and signing:
```bash
sudo /usr/local/bin/ctxos-mirror-update.sh
```

### 4. Export Public Key
Export your public key so clients can trust your mirror:
```bash
gpg --export -a YOUR_KEY_ID > ctxos-repo.gpg
sudo cp ctxos-repo.gpg /var/www/ctxos/
```

### 5. Automate Updates (Cron)
Add a daily cron job to keep your mirror in sync:
```bash
sudo crontab -e
```
Add line:
```cron
0 3 * * * /usr/local/bin/ctxos-mirror-update.sh
```

---

## 🖥️ Client Setup

To configure a client (CtxOS or Debian machine) to use your new mirror:

### 1. Install Signing Key
Download and trust the repository signing key:
```bash
curl -fsSL https://ctxos-mirror.example.com/ctxos-repo.gpg | \
sudo gpg --dearmor -o /usr/share/keyrings/ctxos-mirror.gpg
```

### 2. Add Repository
Create a new source list file pointing to your mirror:
```bash
echo "deb [signed-by=/usr/share/keyrings/ctxos-mirror.gpg] https://ctxos-mirror.example.com ./" | \
sudo tee /etc/apt/sources.list.d/ctxos-mirror.list
```

### 3. Update & Install
```bash
sudo apt update
sudo apt install ctxos
```

---

## 🛠️ Manual Maintenance

### Manually Adding Packages
If you want to add custom `.deb` files to your mirror:
1.  Copy `.deb` files to `/var/www/ctxos/pool/`.
2.  Run the update script: `sudo /usr/local/bin/ctxos-mirror-update.sh`.

### Troubleshooting
*   **Permissions**: Ensure `/var/www/ctxos` is owned by `www-data`: `sudo chown -R www-data:www-data /var/www/ctxos`.
*   **GPG Errors**: Verify the `GPG_KEY_ID` in the script matches `gpg --list-keys`.
*   **404 Errors**: Check NGINX logs: `sudo tail -f /var/log/nginx/error.log`.
