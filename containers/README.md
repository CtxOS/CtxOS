# CtxOS Container Images

This directory provides the code and configuration to build the official **CtxOS Security** container images. These images are designed to be used with any OCI-compliant container engine, like Docker, Podman, or various Kubernetes distributions.

## Image Categories

### [Core](./core)
The `core` image is the foundation for all other CtxOS images. It provides the base Debian system, CtxOS branding, repository configuration, and essential system utilities.
- **Base**: `debian:bookworm-slim`
- **Use Case**: Basis for custom security containers or lightweight CtxOS-based services.

### [Security](./security)
The `security` image is a general-purpose toolkit that contains as many useful CLI security tools as possible.
- **Includes**: Nmap, Masscan, Radare2, GDB, John the Ripper, Gobuster, Nikto, and many more.
- **Use Case**: Interactive security auditing, pentesting from a container, or a ready-to-use security Swiss Army knife.

### [Tools](./tools)
The `tools` folder contains several dedicated lightweight images for specific security tools. These are ideal for CI/CD pipelines or when you only need one specific tool without the overhead of the full security suite.
- **Available Tools**:
  - `nmap`: Security scanning and network discovery.
  - `masscan`: Mass IP/port scanner.
  - `gobuster`: URI and DNS discovery tool.
  - `sqlmap`: Automatic SQL injection and database takeover tool.

## Build Instructions

To build all images in the correct order, run the provided build script:

```bash
./build.sh
```

Alternatively, you can build them individually:

```bash
# Build Core
docker build -t ctxos/core ./core

# Build Security
docker build -t ctxos/security ./security

# Build a Tool (e.g., Nmap)
docker build -t ctxos/tool-nmap ./tools/nmap
```

## Running the Images

### Security Toolkit (Interactive)
```bash
docker run -it --rm ctxos/security
```

### Specific Tool (Non-interactive)
```bash
docker run --rm ctxos/tool-nmap 192.168.1.1
```

## Volumes & Persistence
Most tools write logs or output files. You should mount a volume to `/root` or a specific workspace directory to keep your data:

```bash
docker run -it --rm -v $(pwd):/workspace -w /workspace ctxos/security
```
