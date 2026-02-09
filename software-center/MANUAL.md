# 📖 CtxOS Software Center Manual

The **CtxOS Software Center** is a professional-grade software management toolkit designed for modern Debian derivatives. It provides a secure, proactive, and fail-safe environment for managing system profiles (stacks), native APT packages, and containerized Flatpaks.

---

## 🚀 Getting Started

### Installation
The software center is provided as a standard Debian package. 

```bash
# Update your repository
sudo apt update

# Install the software center
sudo apt install software-center
```

### Manual Installation (Live ISO)
If you are building a custom ISO using `ctxos-dev-kit`, the Software Center is automatically integrated into the build process via `live-iso/build-iso.sh`.

### Launching the UI
The Software Center can be launched from your desktop environment's application menu. Alternatively, you can use the following commands:

1.  **Native GTK4 Experience**:
    - High-performance, follows GNOME Human Interface Guidelines.
    - Executable: `software-center-gtk`
2.  **Premium Webview Experience**:
    - Visual-first design with complex animations and glassmorphism.
    - Executable: `software-center-webview`

---

## 🛠️ Key Concepts

### 1. System Profiles (Stacks)
Unlike traditional app stores, this Software Center is **Profile-Aware**. 
- **Desktop Environment**: A full productivity stack including GUI, browsers, and office tools.
- **Server Base**: A headless, hardened environment for production workloads.
- **Development Stack**: Essential compilers, debuggers, and IDEs.

### 2. Intelligent Migration (Profile Switching)
You can transform your system role at any time. The center handles **Profile Switching** with built-in impact analysis:
- **Impact Analysis**: Shows you exactly which packages will be removed and added.
- **Risk Assessment**: Categorizes changes into Safe, Significant, or Critical system transformations.

### 3. Integrated Flatpak Support
Native access to the **Flathub** ecosystem is built-in. Use the search bar to find and install sandboxed applications alongside traditional system packages.

---

## 🌐 Multi-Platform Development & Testing

CtxOS supports multiple environments for development, testing, and demonstration.

### 🐳 Docker (Containerized Dev)
Build and run the toolkit in an isolated container. Perfect for CI/CD and consistent build environments.

1. **Launch Environment**:
   ```bash
   ./scripts/docker-run.sh
   ```
2. **X11 Forwarding**: The script handles X11 forwarding on Linux and macOS (requires XQuartz).

### 🖥️ VM (Full System Testing)
Test your built ISO in a real-world virtualized environment using QEMU.

1. **Build ISO**:
   ```bash
   cd live-iso && ./build-iso.sh
   ```
2. **Launch VM**:
   ```bash
   ./scripts/run-vm.sh [iso-file]
   ```

### 🪟 WSL (Windows Integration)
Run the toolkit natively on Windows via WSL2.

1. **Install Base Kit**:
   ```bash
   ./scripts/wsl-setup.sh
   ```
### 📱 Multi-Arch Image Building (ARM/RISC-V/RPi)
The toolkit supports building optimized Armbian/Ubuntu images for foreign architectures using QEMU-accelerated chroots.

1. **Build for AArch64 (Raspberry Pi/ARM64)**:
   ```bash
   sudo ./live-iso/armbian-builder/build-image.sh aarch64 ubuntu
   ```
2. **Features**:
   - Cross-architecture chroots via `qemu-user-static`.
   - Automated bootloader configuration for RPi and generic ARM.
   - Inject your custom OS profiles and branding into the final image.

---

## 🚀 Release Management & Fleet Operations

CtxOS includes professional automation for managing the entire distribution lifecycle at scale.

### 🏗️ Master Release Pipeline
The `pipeline-master.sh` script orchestrates the build, validation, and publication of all distribution artifacts:
1. **Automated Building**: Compiles all `.deb` modules and the Software Center.
2. **Containerization**: Generates an updated Docker image for development and CI.
3. **ISO Production**: Builds the latest Live ISO for hardware testing.
4. **Validation**: Runs integrity checks on all artifacts (hashes, file existence, package metadata).

Usage:
```bash
./scripts/pipeline-master.sh patch
```

### 🚢 Production CI/CD
A GitHub Actions workflow is provided in `.github/workflows/production-pipeline.yml`. It automates the master pipeline on every tagged release, uploading build artifacts and verifying system health.

### 🛰️ Fleet Node Management
For large-scale deployments, the toolkit includes a lightweight **Fleet Manager**.
- **Node Dashboard**: Run `python3 scripts/fleet-manager.py` to launch a web interface on port 8080 showing the node's health and version.
- **Monitoring API**: Exposes `/api/status` for integration with central monitoring tools (Prometheus, Nagios).

The Debian Base Kit prioritizes system stability through automated health checks and failsafe mechanisms.

### 🏥 System Health Monitoring
The toolkit includes a `HealthChecker` that validates system vitality after every major operation:
- **Service Verification**: Ensures `dbus`, `polkit`, and `networking` are active.
- **Connectivity Check**: Verifies internet reachability.
- **Post-Migration Validation**: If a profile switch completes but leaves the system unhealthy, the Software Center flags it immediately.

### ⚖️ Transactions & Snapshots
- **Auto-Snapshots**: Every profile switch triggers a persistent system snapshot (Timeshift or Snapper).
- **Graceful Failure**: If a migration step fails, the toolkit stops execution and preserves the pre-migration snapshot for manual or automatic rollback.
- **Atomic Intent**: The toolkit aims for "all-or-nothing" profile switches to prevent partial system breakage.

### System Bus Service
The backend runs as a secure DBus service (`org.ctxos.SoftwareCenter`). This ensures that:
- User frontends never run with root privileges.
- All actions are authenticated via **Polkit** policies.
- System state is managed consistently across multiple open frontends.

### Automatic Restore Points
Safety is non-negotiable. Before any major system migration (Profile Switch):
1.  **Snapshot Creation**: The system automatically detects and uses **Timeshift**, **Snapper**, or **Btrfs** to create a restore point.
2.  **Fail-Safe**: If a snapshot fails, the migration is halted to prevent system instability.
3.  **Atomic Operations**: Actions are batched to ensure the system remains in a valid state.

---

## 🔄 Proactive Maintenance

### Auto-Update Daemon
A background monitor periodically checks for system and app updates.
- **Toast Notifications**: Interactive alerts slide in when updates are ready.
- **Sidebar Badging**: Real-time numeric badges show pending update counts.
- **AppStream Metadata**: Rich descriptions and screenshots are automatically fetched to keep your "Featured" section looking modern.

## 📦 Archive, Mirror & Project Packaging

CtxOS includes a comprehensive system for managing upstream mirrors and custom project builds.

### 🏛️ Package Archive Store
All built artifacts are organized by architecture in the `archive/` directory.

### 🔄 Mirror Sync Engine
Maintain local copies of upstream repositories to speed up builds and installations.
```bash
./scripts/mirror-sync.sh all
```

### 🏗️ Project Packager
Build and publish any project listed in the `projects/manifest.yaml`.
```bash
./scripts/project-packager.sh build "sample-app"
```

### 📋 Project Registry (`projects/manifest.yaml`)
Define your distribution's project ecosystem here. The master pipeline uses this manifest to orchestrate multi-arch builds for all your custom apps and tools.

---

## 📂 Architecture Overview

- **Frontend**: GTK4/Libadwaita or HTML/JS (via PyWebView).
- **Communication**: DBus System Bus.
- **Auth**: PolicyKit (Polkit).
- **Providers**: 
  - `apt`: Native package management.
  - `flatpak`: Flathub integration.
  - `meta`: Profile management.
  - `appstream`: XML metadata & screenshots.
  - `snapshot`: System backup integration.

---

## ❓ FAQ & Troubleshooting

**Q: Why do I see a "System Transformation" warning?**
A: This happens when switching from a Desktop profile to a Server profile. Since it involves removing the graphical interface, the system warns you of the major change.

**Q: Where are the screenshots stored?**
A: Screenshots are dynamically fetched and cached according to the AppStream standard.

**Q: Can I run this on a standard Debian install?**
A: Yes, as long as you have the `pydbus` and `python3-webview` dependencies installed.

### 🛡️ Security & Audit
Trust is built on transparency. The toolkit includes an automated security auditor:
- **`scripts/security-audit.sh`**: Scans the package archive for known vulnerabilities and configuration risks.
- **Pipeline Integration**: Every release is audited before publication to ensure no critical security issues are introduced.

---
*© 2026 CtxOS Team - Advanced Distro Engineering*
