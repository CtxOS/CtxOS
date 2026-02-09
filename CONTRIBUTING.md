# Contributing to CtxOS

Thank you for your interest in contributing to CtxOS! We welcome contributions from the community to make this distribution toolkit even better.

## 🛠️ Development Environment Setup

### Prerequisites
- Debian-based host (Bookworm recommended)
- Python 3.9+
- Node.js & pnpm (for workflow visualizer)
- Docker & QEMU (for testing)

### Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/CtxOS/CtxOS.git
   cd CtxOS
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   (cd workflow && pnpm install)
   ```
3. Run the Software Center in developer mode:
   ```bash
   DEBUG=true python3 software-center/webview_launcher.py
   ```

## 📜 Development Guidelines
- **Modularity**: Keep new features as modules if they are optional system components.
- **Logging**: Use the standard `scripts/log.sh` for bash or the `logging` module for Python.
- **Testing**: Run `./scripts/validate-artifacts.sh` before submitting PRs.
- **Documentation**: Update the `README.md` or relevant `README.md` in modules if the usage changes.

## 🤝 Pull Request Process
1. Create a branch: `git checkout -b feature/your-feature-name`
2. Commit your changes with descriptive messages.
3. Submit a PR against the `main` branch.
4. Ensure CI/CD passes.

---
*By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.*
