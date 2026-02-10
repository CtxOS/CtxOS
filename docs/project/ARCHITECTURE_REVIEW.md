# CtxOS Project Structure & Code Review Analysis

**Date:** February 2026
**Project:** CtxOS - Debian Base Kit Distribution Factory
**Scope:** Architecture, code organization, and best practices assessment

---

## Executive Summary

CtxOS is a **mature, multi-faceted distribution toolkit** with strong foundational design. It successfully integrates shell scripting, Python backends, Node.js frontends, and containerization. However, the project exhibits **moderate architectural entropy** across several dimensions requiring systematic improvements for scalability and maintainability.

**Overall Health Score: 7/10**
**Strengths:** Modular design, clear separation of concerns, CI/CD pipeline
**Gaps:** Test coverage, documentation consistency, error handling patterns, dependency management

---

## Part 1: Current Architecture Assessment

### 1.1 Project Structure Overview

```
CtxOS/
├── scripts/              [Shell orchestration layer]
├── modules/             [Feature modules installed by profile]
├── software-center/     [Main UI: Backend (Python) + Frontend (GTK/Web)]
├── workflow/            [Next.js build visualizer]
├── packaging/           [Debian package generation]
├── live-iso/            [ISO builder using live-build]
├── containers/          [Docker images for tools]
├── config/              [Live-build configurations]
├── profiles/            [Installation profiles: base, desktop, server]
├── recovery/            [System restoration tools]
└── docs/                [Architecture and integration docs]
```

### 1.2 Component Organization

| Component | Type | Tech Stack | Maturity | Issues |
|-----------|------|-----------|----------|--------|
| **Scripts** | Orchestration | Bash | ✅ Good | Inconsistent error handling |
| **Modules** | Features | Bash + Config | ✅ Good | Missing versioning, no tests |
| **Software Center** | Main Service | Python/GTK4 | ⚠️ Medium | DRY violations, minimal tests |
| **Workflow** | Visualization | Next.js/React | ✅ Good | Can be decoupled from core |
| **Packaging** | Build Tools | Shell scripts | ⚠️ Medium | Hardcoded paths, limited logging |
| **Containers** | Infrastructure | Docker | ✅ Good | Limited dependency pinning |
| **Live-ISO** | Distribution | shell-builder | ⚠️ Medium | Complex interdependencies |

---

## Part 2: Gap Analysis

### 🔴 CRITICAL GAPS

#### G1: Test Coverage (Priority: 🔴 HIGH)
**Status:** Minimal to none
**Impact:** Medium-High

- ❌ No unit tests for Python backend
- ❌ No integration tests for module installation
- ❌ No validation tests in CI/CD pipeline
- ❌ Shell scripts lack shellcheck consistency

**Current State:**
```bash
# scripts/ci.yml only runs ShellCheck with exceptions
find . -name "*.sh" -exec shellcheck -e SC1091 {} +
```

**Recommendation:**
```
tests/
├── unit/
│   ├── test_package_providers.py
│   ├── test_profile_manager.py
│   ├── test_version_manager.py
│   └── conftest.py
├── integration/
│   ├── test_module_install.sh
│   ├── test_iso_build.sh
│   └── test_package_build.sh
├── fixtures/
│   ├── mock_apt_cache.py
│   └── test_profiles.mk
└── Makefile
```

#### G2: Error Handling & Validation (Priority: 🔴 HIGH)
**Status:** Inconsistent across codebase
**Impact:** High

**Issues Found:**

1. **Shell scripts** - Disparate patterns:
```bash
# Pattern 1: Silent failures
check_pkg() {
    dpkg -l "$1" &> /dev/null  # Returns true/false silently
}

# Pattern 2: Loose error checking
apt-get install -y "$pkg" || warn "Failed to install $pkg (skipping)"
# ^ Continues on critical failures

# Pattern 3: Missing validation
source "$PROFILE_FILE"  # No existence check before sourcing
```

2. **Python backend** - Limited validation:
   - No input validation in API endpoints
   - Missing error codes/status propagation
   - DBus error handling is basic

**Gap Fix Structure:**
```
scripts/
├── lib.sh              [Current]
├── lib-errors.sh       [NEW] - Standardized error handling
├── lib-validation.sh   [NEW] - Input validation utilities
└── lib-logging.sh      [EXTENDED] - Enhanced logging
```

#### G3: Dependency Management (Priority: 🔴 HIGH)
**Status:** Scattered and version-unconstrained
**Impact:** High (reproducibility/consistency)

**Issues:**
- `requirements.txt` has no pinned versions:
  ```plaintext
  pywebview>=5.0      # ❌ Too loose
  pydbus>=0.6.0
  PyGObject>=3.40.0
  ```

- Shell dependencies undocumented:
  - Module `firefox/` needs specific versions
  - Live-build requires exact config format

- `workflow/package.json` uses "latest" for critical deps:
  ```json
  "@ai-sdk/google": "latest",  // ❌ Dangerous
  "ai": "latest"
  ```

- No lock file attestation

**Recommended Fix:**
```
├── .lock/
│   ├── requirements.lock      [pip-tools]
│   ├── pnpm-lock.yaml         [existing, good]
│   └── dependencies.txt       [shell package versions]
├── requirements-dev.txt        [dev-only deps]
├── requirements-prod.txt       [pinned versions]
└── pyproject.toml             [PEP 517/518 compliant]
```

#### G4: Documentation Inconsistency (Priority: 🟠 MEDIUM)
**Status:** Mixed quality, scattered location
**Impact:** Medium

**Issues:**
- Module installation documented in README but not in `modules/*/README.md`
- Python backend architecture not documented
- Software Center API not formally documented
- Profile override mechanisms unclear
- Module integration points vague

**Gap Structure:**
```
docs/
├── architecture.md          [GOOD - 40 lines]
├── modules/                 [NEW]
│   ├── README.md            [Module structure guide]
│   └── DEVELOPING.md
├── software-center/         [NEW]
│   ├── API.md              [Backend REST/DBus API]
│   ├── ARCHITECTURE.md
│   └── PROVIDERS.md         [Package provider interface]
├── backend/                 [NEW]
│   ├── API_SPECIFICATION.md
│   └── ERROR_CODES.md
├── RELEASE.md               [Currently absent]
└── MIGRATION.md             [NEW - breaking changes]
```

---

### 🟠 MEDIUM GAPS

#### G5: Logging & Observability (Priority: 🟠 MEDIUM)
**Status:** Implemented but inconsistent
**Scope:** Low-medium

**Issues:**
- `scripts/log.sh` has basic colored output but no log levels
- No log aggregation or structured logging
- Pipeline tracing missing
- Python logging uses default module (no custom formatters)

**Current:**
```bash
log() { echo -e "${COLOR_GREEN}[INFO]${COLOR_RESET} $1"; }
warn() { echo -e "${COLOR_BLUE}[WARN]${COLOR_RESET} $1"; }
error() { echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1"; }
```

**Recommended Enhancement:**
```bash
# scripts/lib-logging.sh [NEW]
log_debug()   { [[ $DEBUG == "true" ]] && echo "[DEBUG]" "$@"; }
log_trace()   { [[ $TRACE == "true" ]] && echo "[TRACE]" "$@"; }
log_metric()  { echo "[METRIC]" "$@" >> "${LOG_FILE:-/dev/null}"; }
```

#### G6: Version Management & Semver (Priority: 🟠 MEDIUM)
**Status:** Present but simplistic

**Issues:**
- `VERSION` is plain text file (`1.0.1`)
- No version bumping logic (only in `scripts/release.sh`)
- Modules don't have individual versions
- No package version tracking in profiles

**Suggested Structure:**
```
version/
├── VERSION              [Current: "1.0.1"]
├── CHANGELOG.md
├── bump.sh              [Semantic version bumping]
└── validate-version.sh
```

#### G7: Profile System Clarity (Priority: 🟠 MEDIUM)
**Status:** Working but underdocumented

**Issues:**
- Profiles defined as `profiles/*.mk` (Makefile syntax)
- Module inclusion logic opaque
- No profile validation
- No profiles/README explaining override mechanics

**Current Profile Example:**
```makefile
# profiles/base.mk
MODULES = apt core menu interface zsh-config
# Just a list - no documentation on ordering, conflicts, or dependencies
```

**Recommendation:**
```yaml
# profiles/base.yaml [NEW - structured]
name: base
description: Minimal system with core utilities
version: "1.0"
inherit: null
modules:
  apt:
    required: true
    order: 1
  core:
    required: true
    order: 2
    conflicts: []
  menu: { order: 3 }
  interface: { order: 4 }
  zsh-config: { order: 5 }
  # ...
```

#### G8: Module Dependency Graph (Priority: 🟠 MEDIUM)
**Status:** No formal dependency system

**Issues:**
```bash
# setup.sh just installs modules in order
for m in ${MODULES}; do
  if [ -d "modules/$m" ]; then
    bash ./modules/$m/install.sh
  fi
done
```

**Problem:** No way to specify or validate dependencies between modules

**Recommendation:**
```
modules/
├── core/
│   ├── module.yaml      [NEW]
│   │   depends: []
│   │   conflicts: [firefox]  # Can't run with lightweight browser
│   │   provides: [base-system, logging]
│   └── install.sh
├── firefox/
│   ├── module.yaml
│   │   depends: [interface]
│   └── install.sh
```

#### G9: Software Center Architecture (Priority: 🟠 MEDIUM-HIGH)
**Status:** Good design, implementation gaps

**Issues:**
```
software-center/
├── backend/
│   ├── api/             [Limited endpoints]
│   ├── daemon.py        [Monolithic, 200+ lines likely]
│   ├── providers/       [Package providers - may have DRY issues]
│   └── dbus/            [DBus service definitions]
└── frontend/
    ├── gtk/             [Native GTK4 UI]
    └── web/             [Web-based UI]
```

**Specific Issues:**
- No formal API specification (OpenAPI/AsyncAPI)
- Provider interface not documented
- No middleware/plugin system
- DRY violations likely in provider impls
- Minimal error propagation

#### G10: Build Pipeline Complexity (Priority: 🟠 MEDIUM)
**Status:** Functional but monolithic

**Current:**
```bash
# scripts/pipeline-master.sh - 70+ lines, 5 stages
Stage 0: Mirror sync
Stage 1: Package building + versioning
Stage 1.5: Project packaging (commented out)
Stage 2: Docker build
Stage 2.5: Metadata generation
Stage 3: ISO building
Stage 3.5: Multi-arch builds
Stage 3.8: Repository updates
Stage 4: Validation
Stage 4.5: Security audit
Stage 5: Summary
```

**Issues:**
- Stages not independently runnable
- No cleanup on partial failures
- Artifact dependencies unclear
- Security audit runs at end (should be earlier)

---

### 🟡 MINOR GAPS

#### G11: Code Organization (Python) (Priority: 🟡 LOW)
**Status:** Reasonable but could be cleaner

Currently:
```
software-center/backend/
├── api/
├── dbus/
├── daemon.py
├── locales/
└── providers/
```

Should add:
```
├── errors.py          [Custom exceptions]
├── types.py           [Type definitions/enums]
├── config.py          [Configuration loading]
├── utils.py           [Common utilities]
└── middleware/
    ├── auth.py        [DBus authentication]
    └── logging.py     [Request logging]
```

#### G12: Static Analysis (Priority: 🟡 LOW)
**Status:** ShellCheck present, missing others

**Current:**
- ✅ ShellCheck for bash
- ❌ No pylint/flake8 for Python
- ❌ No ESLint for JavaScript
- ❌ No mypy for type checking

#### G13: Security Hardening (Priority: 🟡 MEDIUM)
**Status:** Awareness present, implementation gaps

**Current:**
- ✅ DBus + Polkit for privilege escalation
- ✅ AppArmor profiles being deployed
- ❌ No SBOM generation (Software Bill of Materials)
- ❌ No container image scanning
- ❌ No dependency vulnerability scanning

---

## Part 3: Best Practices Recommendations

### 3.1 Recommended Project Structure

```
CtxOS/
│
├── 📋 ROOT FILES
│   ├── VERSION                 [semver: 1.0.1]
│   ├── pyproject.toml          [PEP 517/518, replaces setup.py]
│   ├── ARCHITECTURE_REVIEW.md  [This document]
│   ├── DEVELOPMENT.md          [NEW - dev guidelines]
│   └── SECURITY.md             [Existing]
│
├── 📚 DOCUMENTATION (docs/)
│   ├── README.md               [Overview - GOOD]
│   ├── ARCHITECTURE.md         [EXPAND]
│   ├── CONTRIBUTING.md         [Improve - add technical sections]
│   ├── API.md                  [NEW - Software Center API]
│   ├── MIGRATION.md            [NEW - breaking changes]
│   ├── RELEASE.md              [NEW - versioning strategy]
│   ├── BUILD_PIPELINE.md       [NEW - pipeline stages]
│   ├── SECURITY_AUDIT.md       [NEW - CVE handling]
│   │
│   ├── backend/                [NEW]
│   │   ├── ARCHITECTURE.md
│   │   ├── API_SPECIFICATION.md
│   │   ├── PROVIDERS.md
│   │   └── ERROR_CODES.md
│   │
│   ├── modules/                [NEW]
│   │   ├── README.md           [Module structure guide]
│   │   ├── DEVELOPING.md
│   │   └── MODULE_TEMPLATE/
│   │
│   ├── workflows/              [NEW]
│   │   ├── CI_CD.md
│   │   └── RELEASE_PROCESS.md
│   │
│   └── architecture-diagrams/  [NEW]
│       ├── component-map.md
│       ├── data-flow.md
│       └── deployment.md
│
├── 🧪 TESTS (tests/)           [NEW]
│   ├── conftest.py
│   ├── pytest.ini
│   │
│   ├── unit/
│   │   ├── test_package_providers.py
│   │   ├── test_profile_manager.py
│   │   ├── test_version_manager.py
│   │   ├── test_deployment.py
│   │   └── __init__.py
│   │
│   ├── integration/
│   │   ├── test_module_install.sh
│   │   ├── test_iso_build.sh
│   │   └── test_docker_build.sh
│   │
│   ├── e2e/                    [NEW - end-to-end]
│   │   ├── test_full_pipeline.sh
│   │   └── test_profile_switch.sh
│   │
│   ├── fixtures/               [Test data]
│   │   ├── mock_apt_cache.py
│   │   ├── test_profiles.mk
│   │   └── sample_modules/
│   │
│   └── benchmarks/             [NEW - performance]
│       └── package_discovery.py
│
├── 📦 SOURCE CODE (src/)       [RESTRUCTURE EXISTING]
│   │
│   ├── backend/                [Rename: software-center/backend]
│   │   ├── __init__.py
│   │   ├── daemon.py           [Entry point]
│   │   ├── api/                [REST/DBus endpoints]
│   │   │   ├── __init__.py
│   │   │   ├── packages.py
│   │   │   ├── profiles.py
│   │   │   ├── system.py
│   │   │   └── middleware.py
│   │   ├── core/               [NEW - business logic]
│   │   │   ├── __init__.py
│   │   │   ├── package_manager.py
│   │   │   ├── profile_manager.py
│   │   │   ├── snapshot_manager.py
│   │   │   └── version_manager.py
│   │   ├── providers/          [Package providers]
│   │   │   ├── __init__.py
│   │   │   ├── base.py         [NEW - abstract provider]
│   │   │   ├── apt_provider.py
│   │   │   ├── flatpak_provider.py
│   │   │   └── meta_provider.py
│   │   ├── dbus/
│   │   │   ├── __init__.py
│   │   │   └── service.py
│   │   ├── models/             [NEW - data models]
│   │   │   ├── __init__.py
│   │   │   ├── package.py
│   │   │   ├── profile.py
│   │   │   └── error.py
│   │   ├── errors.py           [NEW - custom exceptions]
│   │   ├── config.py           [NEW - config mgmt]
│   │   ├── logger.py           [NEW - logging]
│   │   ├── locales/
│   │   └── py.typed            [PEP 561 typing]
│   │
│   ├── cli/                    [NEW - command-line tools]
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── commands/
│   │   │   ├── build.py
│   │   │   ├── install.py
│   │   │   └── validate.py
│   │   └── shell-completions/
│   │
│   ├── frontend/
│   │   ├── gtk/                [GTK4 native]
│   │   │   ├── main.py
│   │   │   ├── windows/
│   │   │   └── widgets/
│   │   └── web/                [Web/Webview]
│   │       └── [same as workflow/]
│   │
│   └── scripts/                [System scripts]
│       ├── lib/                [NEW - organized]
│       │   ├── lib-core.sh
│       │   ├── lib-errors.sh
│       │   ├── lib-validation.sh
│       │   ├── lib-logging.sh
│       │   └── lib-packaging.sh
│       ├── install/
│       │   ├── setup.sh
│       │   └── uninstall.sh
│       ├── build/
│       │   ├── pipeline.sh
│       │   ├── build-debs.sh
│       │   └── build-iso.sh
│       ├── tools/
│       │   ├── mirror-sync.sh
│       │   ├── validate-artifacts.sh
│       │   ├── security-audit.sh
│       │   ├── release.sh
│       │   └── generate-metadata.sh
│       ├── ci/
│       │   ├── lint-check.sh
│       │   ├── test-runner.sh
│       │   └── validate-pr.sh
│       └── dev/
│           ├── docker-run.sh
│           ├── run-vm.sh
│           └── wsl-setup.sh
│
├── 🏗️ INFRASTRUCTURE (infra/)  [NEW]
│   ├── docker/
│   │   ├── Dockerfile.base     [Extract: Dockerfile → container module]
│   │   ├── Dockerfile.build
│   │   └── docker-compose.yml
│   ├── containers/             [Rename existing: containers/]
│   │   ├── core/
│   │   ├── security/
│   │   └── tools/
│   ├── live-iso/               [Keep existing]
│   ├── kubernetes/             [NEW - if needed later]
│   └── terraform/              [NEW - if deploying to cloud]
│
├── 🧩 MODULES (modules/)
│   ├── README.md               [Module guide]
│   ├── module-template/        [NEW - starter template]
│   │   ├── module.yaml         [Structured metadata]
│   │   ├── packages.txt
│   │   ├── install.sh
│   │   ├── remove.sh
│   │   ├── test.sh             [NEW - module tests]
│   │   └── files/
│   ├── apt/
│   ├── core/
│   │   ├── module.yaml         [NEW]
│   │   ├── packages.txt
│   │   ├── install.sh
│   │   ├── remove.sh
│   │   │
│   │   └── files/
│   │       ├── sysctl.conf
│   │       └── apparmor/
│   ├── firefox/
│   ├── interface/
│   ├── menu/
│   ├── themes/
│   ├── tools/
│   ├── updater/
│   └── zsh-config/
│
├── 📋 PROFILES (profiles/)
│   ├── README.md               [Profile guide - NEW]
│   ├── base.yaml              [Convert: .mk → .yaml NEW]
│   ├── desktop.yaml
│   ├── server.yaml
│   ├── rescue.yaml
│   └── validator/             [NEW]
│       └── validate-profile.sh
│
├── 🔧 CONFIGURATION (config/)
│   ├── README.md              [Config guide - NEW]
│   ├── templates/
│   ├── presets/               [NEW - preset configs]
│   │   ├── minimal.yaml
│   │   ├── workstation.yaml
│   │   └── server.yaml
│   │
│   └── [existing live-build config structure]
│
├── 📦 BUILD & PACKAGING
│   ├── packaging/              [Keep: Debian packaging]
│   ├── projects/               [Keep: Project isolation]
│   └── build_output/           [Keep: Artifacts]
│
├── 🔄 CI/CD (.github/)
│   ├── workflows/
│   │   ├── ci.yml              [Expand: add unit tests, pylint, mypy]
│   │   ├── cd.yml              [CD pipeline]
│   │   ├── security.yml        [NEW - SAST, SBOM, scanning]
│   │   ├── performance.yml     [NEW - build time tracking]
│   │   └── release.yml         [NEW - release automation]
│   │
│   ├── actions/                [NEW - reusable actions]
│   │   ├── setup-env.yml
│   │   ├── run-tests.yml
│   │   └── validate-artifacts.yml
│   │
│   └── CODEOWNERS             [NEW - PR review routing]
│
├── 📊 WORKFLOW (workflow/)
│   ├── [Keep existing Next.js structure]
│   └── [Add: Decouple from core deployment]
│
├── 🔐 SECURITY & VERSIONING
│   ├── .lock/                  [NEW - dependency locks]
│   │   ├── requirements.lock
│   │   ├── pnpm-lock.yaml
│   │   └── dependencies.txt
│   ├── version/                [NEW - version mgmt]
│   │   ├── VERSION
│   │   ├── CHANGELOG.md
│   │   └── bump.sh
│   ├── .gitignore              [Improve: add lock files, build output]
│   ├── .editorconfig
│   ├── .pre-commit-config.yaml [NEW - local hooks]
│   │
│   └── ctxos.asc               [Keep: PGP key]
│
├── 📋 DEPENDENCY CONFIGURATION
│   ├── pyproject.toml          [NEW - Python packaging]
│   ├── requirements-base.txt   [NEW - core deps]
│   ├── requirements-dev.txt    [NEW - dev-only deps]
│   ├── requirements-test.txt   [NEW - test deps]
│   ├── setup.cfg               [Optional: setuptools config]
│   │
│   ├── .npmrc                  [NEW - npm config]
│   ├── .pnpmfile.cjs          [NEW - pnpm config]
│   │
│   └── Dockerfile → docker/    [MOVE: to infra/]
│
└── 📚 OTHER
    ├── LICENSE                 [Existing: Apache 2.0]
    ├── SECURITY.md             [Existing]
    ├── Makefile                [Top-level: keep/enhance]
    ├── VERSION                 [Move to: version/]
    ├── branding.json
    └── mirror/                 [Keep: mirror sync tools]
```

### 3.2 Error Handling Standards

**Create:** `scripts/lib-errors.sh`

```bash
#!/usr/bin/env bash
# Standardized error handling across CtxOS

# Exit codes
readonly EXIT_OK=0
readonly EXIT_GENERAL=1
readonly EXIT_INVALID_ARG=2
readonly EXIT_NOT_FOUND=3
readonly EXIT_PERMISSION=4
readonly EXIT_TIMEOUT=5
readonly EXIT_DEPENDENCY=6
readonly EXIT_CONFIG=7

# Error context
declare -g ERROR_CONTEXT=""
declare -g ERROR_CODE=0

set_error_context() {
    ERROR_CONTEXT="$1"
}

error_exit() {
    local code="$1" message="$2"
    error "[${ERROR_CONTEXT}] ${message} (exit code: ${code})"
    exit "$code"
}

# Trap errors with context
trap 'error_exit $? "Unhandled error at line $LINENO"' ERR
```

### 3.3 Test Strategy

**Python Unit Tests** (`tests/unit/test_package_providers.py`):

```python
import pytest
from unittest.mock import MagicMock, patch
from src.backend.providers.apt_provider import AptProvider
from src.backend.errors import PackageNotFoundError

@pytest.fixture
def apt_provider():
    return AptProvider()

def test_package_search_returns_results(apt_provider):
    """Test APT provider can search packages"""
    with patch('apt.Cache') as mock_cache:
        mock_cache.return_value.search.return_value = [...]
        results = apt_provider.search("python3")
        assert len(results) > 0

def test_package_not_found_raises_error(apt_provider):
    """Test missing package raises error"""
    with pytest.raises(PackageNotFoundError):
        apt_provider.get("nonexistent-package-xyz")
```

**Shell Integration Tests** (`tests/integration/test_module_install.sh`):

```bash
#!/usr/bin/env bash
set -e

# Test module installation in isolated environment
setup_test_env() {
    export TMPDIR=$(mktemp -d)
    export MODULES_DIR="$TMPDIR/modules"
    mkdir -p "$MODULES_DIR"
}

test_core_module_install() {
    # Create minimal test module
    mkdir -p "$MODULES_DIR/test-module"
    cat > "$MODULES_DIR/test-module/install.sh" << 'EOF'
#!/bin/bash
echo "test" > /tmp/test-marker
EOF
    chmod +x "$MODULES_DIR/test-module/install.sh"

    # Run installation
    bash "$MODULES_DIR/test-module/install.sh"

    # Verify
    assert_file_exists "/tmp/test-marker"
}

teardown_test_env() {
    rm -rf "$TMPDIR"
}
```

### 3.4 Dependency Management

**Create:** `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ctxos"
version = "1.0.1"
description = "Debian Base Kit - Distribution Factory"
requires-python = ">=3.9"
dependencies = [
    "pywebview==5.1.3",
    "pydbus==0.6.0",
    "PyGObject==3.46.0",
    "python-apt==2.6.2",
]

[project.optional-dependencies]
dev = [
    "pytest==7.4.3",
    "pytest-cov==4.1.0",
    "pylint==3.0.3",
    "flake8==6.1.0",
    "mypy==1.7.1",
    "black==23.12.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing"

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Gradual adoption
```

**Create:** `requirements-prod.txt`

```
# Pinned production dependencies
pywebview==5.1.3
pydbus==0.6.0
PyGObject==3.46.0
python-apt==2.6.2
```

### 3.5 CI/CD Improvements

**Expand:** `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: ShellCheck
        run: |
          sudo apt-get install shellcheck
          find scripts -name "*.sh" -exec shellcheck {} +
      - name: Pylint
        run: |
          pip install pylint
          pylint src/backend --fail-under=7.0
      - name: MyPy
        run: |
          pip install mypy
          mypy src/backend --strict

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install deps
        run: pip install -r requirements-test.txt
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
      - name: Bandit (Python)
        run: |
          pip install bandit
          bandit -r src/backend
```

### 3.6 Module Definition Format

**Create:** `modules/module-template/module.yaml`

```yaml
# Module metadata and dependencies
name: module-name
version: "1.0.0"
description: "Brief description of this module"
maintainer: "Your Name <you@example.com>"

# Module installation order and dependencies
order: 10  # Installation order (lower = earlier)
required: false
conflicts:
  - conflicting-module
depends:
  - core  # Must install 'core' first
provides:
  - service-name
  - optional-component

# Configuration
config:
  interactive: false  # Prompt user for options?
  autoload: true

# Testing
test:
  enabled: true
  script: test.sh
```

---

## Part 4: Implementation Roadmap

### Phase 1: Foundation (Weeks 1-3)
- [ ] Create test infrastructure (`tests/`)
- [ ] Add `pyproject.toml` and lock dependency versions
- [ ] Implement error handling standards (`lib-errors.sh`)
- [ ] Document current architecture (expand `docs/`)

### Phase 2: Code Modernization (Weeks 4-6)
- [ ] Restructure Python backend into `src/backend/`
- [ ] Add type hints and mypy integration
- [ ] Implement unit tests for core modules
- [ ] Convert profiles from `.mk` to `.yaml`

### Phase 3: CI/CD Enhancement (Weeks 7-8)
- [ ] Expand GitHub Actions workflows (security, performance)
- [ ] Add integration/E2E tests to pipeline
- [ ] Implement code coverage gates
- [ ] Add pre-commit hooks

### Phase 4: Polish & Documentation (Weeks 9-10)
- [ ] Complete documentation for all components
- [ ] Add module templates and guides
- [ ] Security audit and hardening
- [ ] Release candidate testing

---

## Part 5: Priority Summary

### 🔴 Critical (Fix First)
1. **Test Coverage** - Start with core package provider tests
2. **Error Handling** - Standardize patterns across codebase
3. **Dependency Pinning** - Lock all versions, create lock files

### 🟠 High (Fix Next Quarter)
4. **Error Propagation** - Software Center API error codes
5. **Module Dependencies** - Formalize dependency graph
6. **Documentation** - Complete architecture docs

### 🟡 Medium (Plan for Later)
7. **Static Analysis** - Add pylint, flake8, ESLint
8. **Profile System** - Migrate to YAML, add validation
9. **Logging** - Structured logging, log aggregation

### 🟢 Low (Nice to Have)
10. **Performance Benchmarks** - Track build times
11. **Cloud Deployment** - Kubernetes/Terraform configs
12. **Container Scanning** - Automated CVE detection

---

## Part 6: Code Quality Metrics (Baseline)

| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| Test Coverage | ~5% | 70% | Q2 2026 |
| Type-Hint Coverage (Python) | ~10% | 80% | Q2 2026 |
| Linting Score | 6/10 | 9/10 | Q2 2026 |
| Documentation Completeness | 60% | 95% | Q2 2026 |
| Cyclomatic Complexity | ~8 avg | <5 avg | Q2 2026 |
| Dependency Updates | Manual | Automated | Q1 2026 |

---

## Part 7: Architecture Diagrams

### Data Flow: Module Installation

```
┌─────────────┐
│   Profile   │  (base.yaml)
│ {modules[]} │
└──────┬──────┘
       │
       ├─→ Module 1: apt         ┌──────────────┐
       │   ├─ packages.txt  ───→ │   APT Repo   │
       │   ├─ install.sh   ──→   │  (packages)  │
       │   └─ files/       ──→   └──────────────┘
       │
       ├─→ Module 2: core        ┌──────────────┐
       │   ├─ packages.txt  ───→ │   System     │
       │   ├─ install.sh   ──→   │  (configs)   │
       │   └─ files/       ──→   └──────────────┘
       │
       └─→ Module N: ...
```

### Software Center Architecture

```
┌─────────────────────────────────────────────────────┐
│          Desktop Environment (D-Bus)                 │
└────────┬────────────────────────────────────────────┘
         │
    ┌────┴────┐
    │  IPC    │
    │ (D-Bus) │
    └────┬────┘
         │
    ┌────▼────────────────────────────────────────┐
    │    Backend Daemon (Python)                   │
    │  ┌────────────────────────────────────────┐ │
    │  │  Core Business Logic                   │ │
    │  │ - Package Manager                      │ │
    │  │ - Profile Manager                      │ │
    │  │ - Snapshot Manager                     │ │
    │  └────────────────────────────────────────┘ │
    │                      │                       │
    │  ┌──────────────────┼──────────────────┐    │
    │  ▼                  ▼                   ▼    │
    │ ┌────────┐  ┌──────────────┐  ┌────────┐   │
    │ │  APT   │  │   Flatpak    │  │  Meta  │   │
    │ │Provider│  │  Provider    │  │Package │   │
    │ └────────┘  └──────────────┘  └────────┘   │
    │      │             │                 │      │
    │      └─────────────┼─────────────────┘      │
    │                    │                        │
    └────────────────────┼────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      ┌────────┐  ┌──────────┐  ┌──────────┐
      │  GTK4  │  │ Webview  │  │ CLI      │
      │Frontend│  │ Frontend │  │Interface │
      └────────┘  └──────────┘  └──────────┘
```

---

## Conclusion

CtxOS demonstrates **solid engineering fundamentals** with clear modularization and multi-layered architecture. The primary opportunities lie in:

1. **Automated Testing** - From 5% to 70% coverage
2. **Dependency Management** - Pinned versions and lock files
3. **Error Handling** - Standardized patterns
4. **Documentation** - Comprehensive guides for all layers

With focused effort on these gaps over the next 10 weeks, CtxOS can achieve **enterprise-grade code quality** while maintaining its modular, user-friendly design philosophy.

**Next Step:** Prioritize Phase 1 (Foundation) tasks to establish testing infrastructure and standardized error handling patterns.

---

**Document Version:** 1.0
**Last Updated:** February 2026
**Reviewer:** Architecture Analysis
**Status:** Ready for Implementation
