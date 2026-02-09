# 🚀 CtxOS — The Ultimate Distribution Factory

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE.txt)  
[![Build Status](https://github.com/CtxOS/CtxOS/actions/workflows/software-center.yml/badge.svg)](https://github.com/CtxOS/CtxOS/actions)  
[![Latest Release](https://img.shields.io/github/v/release/CtxOS/CtxOS)](https://github.com/CtxOS/CtxOS/releases)

---

## Overview

The **Debian Base Kit** is a professional-grade, modular toolkit to build, manage, and ship custom Debian-based Linux distributions across multiple architectures.

From single commands to automated pipelines, it empowers distro maintainers and developers with:

- Multi-architecture (x86_64, ARM64, RISC-V, Raspberry Pi) image builds  
- Unified package management (APT + Flatpak + Meta-packages)  
- Advanced system services secured via DBus & Polkit  
- Proactive auto-updates, snapshot-protected migrations & rollback  
- Fully localized UI with hardware-aware intelligent stack suggestions  
- Integrated CI/CD pipeline with release orchestration and live ISO generation  
- Docker, VM, and WSL2 development environments for portability  
- Centralized archive, mirror sync, and project packaging system  

---

## 🏗 Architecture at a Glance

| Component             | Description                                                   |
|-----------------------|---------------------------------------------------------------|
| **Backend Service**   | Secure DBus + Polkit gated system services                    |
| **Frontends**         | Native GTK4 + Premium Webview UI with rich AppStream metadata |
| **Snapshot Manager**  | Timeshift/Snapper-based system restore and rollback           |
| **Package Providers** | APT, Flatpak, Meta-packages unified into one discovery engine |
| **Localization**      | Multilingual UI with EN/ES support, scalable to more languages|
| **Release Pipeline**  | Automated version bumping, build, packaging, and deployment   |
| **Multi-Arch Builder**| Cross-architecture rootfs and ISO builder with QEMU emulation |
| **Archive & Mirror**  | Central repo with upstream mirror syncing                      |
| **Project Packager**  | Build, test, and archive your distro projects                  |

---

## 🎯 Key Features

### Multi-Format Package Management  
Seamlessly manage APT and Flatpak packages alongside custom meta-packages with smart installation logic.

### Intelligent Profile Switching  
Switch between Server, Desktop, and Developer profiles with guided impact analysis and snapshot safety.

### Self-Healing System  
Live update monitoring with transactional package installs and automatic rollback on failure.

### Global Localization  
Dynamic, JSON-driven translations with fallback and support for adding your own languages.

### Cross-Platform Development  
Develop and test inside Docker containers, Virtual Machines, or Windows Subsystem for Linux (WSL2).

### Automated Release & CI/CD  
One-command full release orchestration with changelog generation, artifact publishing, and ISO creation.

---

## 🚀 Getting Started

### Prerequisites

- Debian-based development host (Ubuntu, Debian, etc.)  
- Python 3.9+ and dependencies (`pip install -r requirements.txt`)  
- Docker (optional, for containerized dev environment)  
- QEMU + KVM (optional, for VM testing)  

### Quickstart

### 📊 Build Pipeline Visualizer
CtxOS includes an interactive workflow visualizer to understand and manage the build process:
```bash
cd workflow
pnpm install
pnpm dev
```
Then visit:
- `http://localhost:3000/ctxos` - CtxOS Build Pipeline
- `http://localhost:3000` - AI Agent Builder (general purpose)

See `workflow/README.md` and `workflow/INTEGRATION.md` for details.

### Installation
To install the default (**base**) profile:
```bash
# Clone the repository
git clone https://github.com/CtxOS/CtxOS.git
cd CtxOS

# Build and launch the Software Center Webview UI
pip install pywebview
python3 software-center/webview_launcher.py
````

### Building a Multi-Arch Image

```bash
# Build images for Raspberry Pi, ARM64, and RISC-V
BUILD_MULTI_ARCH=true ./scripts/pipeline-master.sh
```

### Running in Docker

```bash
./scripts/docker-run.sh
```

---

## 📚 Documentation

For comprehensive setup, usage, and architecture details, see [MANUAL.md](software-center/MANUAL.md).

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting pull requests.

---

## 📄 License

This project is licensed under the Apache 2.0 License — see the [LICENSE.txt](LICENSE.txt) file for details.

---

## 🎉 Join the Community

Stay updated and contribute:

* GitHub Issues & Pull Requests
* Community Forum (link)
* Mailing List (link)

---

*Crafted with ❤️ for the open source Linux community.*
