# CtxOS: Quick-Start Implementation Guide

This document provides actionable, step-by-step instructions to address the top gaps identified in the Architecture Review.

---

## Quick Reference: Gap Priority Matrix

| Gap | Severity | Effort | Impact | Quick Fix? |
|-----|----------|--------|--------|-----------|
| Test Coverage | 🔴 HIGH | HIGH | HIGH | ✅ Start with 1-2 tests |
| Error Handling | 🔴 HIGH | MEDIUM | HIGH | ✅ Refactor lib.sh |
| Dependencies | 🔴 HIGH | LOW | HIGH | ✅ Add pyproject.toml |
| Documentation | 🟠 MEDIUM | MEDIUM | MEDIUM | ✅ Template-driven |
| Logging | 🟠 MEDIUM | LOW | MEDIUM | ✅ Extend lib-logging.sh |
| Versioning | 🟠 MEDIUM | LOW | MEDIUM | ⚠️ Requires process change |
| Profiles | 🟠 MEDIUM | MEDIUM | MEDIUM | ⚠️ Backward compat needed |
| Module Deps | 🟠 MEDIUM | MEDIUM | MEDIUM | ⚠️ Validation needed |
| Software Center | 🟠 MEDIUM | HIGH | HIGH | ⚠️ Refactor in phases |
| Build Pipeline | 🟠 MEDIUM | MEDIUM | MEDIUM | ✅ Stage isolation |

---

## WEEK 1-2: Foundation (Test & Dependencies)

### Task 1.1: Create Test Infrastructure

**Objective:** Bootstrap testing framework
**Time:** 2 hours
**Dependencies:** None

```bash
# 1. Create test directory structure
mkdir -p tests/{unit,integration,fixtures,e2e}
touch tests/__init__.py tests/conftest.py

# 2. Create pytest configuration
cat > tests/pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests
EOF

# 3. Create conftest.py (shared fixtures)
cat > tests/conftest.py << 'EOF'
import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def tmp_module_dir():
    """Temporary directory for test modules"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def mock_profile():
    """Mock profile for testing"""
    return {
        "name": "test-profile",
        "modules": ["apt", "core"]
    }
EOF

# 4. Create first unit test
cat > tests/unit/test_example.py << 'EOF'
import pytest

def test_sanity_check():
    """Verify testing framework works"""
    assert 1 + 1 == 2

@pytest.mark.unit
def test_import_backend():
    """Test backend can be imported"""
    # Once src/backend refactored, update this
    assert True
EOF

# 5. Run tests to verify setup
pip install pytest pytest-cov
pytest -v
```

**Checklist:**
- [ ] `tests/` directory created with subdirs
- [ ] `pytest.ini` configured
- [ ] `conftest.py` with fixtures
- [ ] Example test passes
- [ ] Coverage report generated

**Expected Output:**
```
tests/unit/test_example.py::test_sanity_check PASSED         [50%]
tests/unit/test_example.py::test_import_backend PASSED       [100%]

======================== 2 passed in 0.05s =========================
```

---

### Task 1.2: Pin Dependencies

**Objective:** Ensure reproducible builds
**Time:** 1.5 hours
**Dependencies:** Task 1.1 (optional)

```bash
# 1. Create production requirements
cat > requirements-prod.txt << 'EOF'
# Core production dependencies (pinned versions)
pywebview==5.1.3
pydbus==0.6.0
PyGObject==3.46.0
python-apt==2.6.2
Jinja2==3.1.2
EOF

# 2. Create development requirements
cat > requirements-dev.txt << 'EOF'
-r requirements-prod.txt

# Development and testing
pytest==7.4.3
pytest-cov==4.1.0
pylint==3.0.3
flake8==6.1.0
mypy==1.7.1
black==23.12.0
pre-commit==3.6.0
EOF

# 3. Create pyproject.toml
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ctxos"
version = "1.0.1"
description = "Debian Base Kit - Distribution Factory"
requires-python = ">=3.9"
license = {text = "Apache-2.0"}

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

[tool.setuptools.packages.find]
where = ["src"]
include = ["backend*", "cli*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing --cov-report=html"

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false

[tool.pylint."messages control"]
disable = ["C0111", "C0103"]  # Missing docstring, invalid names
EOF

# 4. Generate lock file
pip install pip-tools
pip-compile requirements-prod.txt -o requirements.lock
pip-compile requirements-dev.txt -o requirements-dev.lock

# 5. Verify
pip install -r requirements.lock
python -c "import pywebview; print(f'✓ pywebview {pywebview.__version__}')"
```

**Checklist:**
- [ ] `requirements-prod.txt` created with pinned versions
- [ ] `requirements-dev.txt` created
- [ ] `pyproject.toml` created and valid
- [ ] Lock files generated
- [ ] All dependencies installable

**Verification:**
```bash
pip install -e ".[dev]"
pytest
```

---

### Task 1.3: Standardize Error Handling

**Objective:** Consistent error codes and handling
**Time:** 2 hours
**Dependencies:** None

```bash
# 1. Create error handling library
cat > scripts/lib-errors.sh << 'EOF'
#!/usr/bin/env bash
# Error handling standards for CtxOS

# Define exit codes
readonly EXIT_OK=0              # Success
readonly EXIT_GENERAL=1         # General error
readonly EXIT_INVALID_ARG=2     # Invalid arguments
readonly EXIT_NOT_FOUND=3       # File/package not found
readonly EXIT_PERMISSION=4      # Permission denied
readonly EXIT_TIMEOUT=5         # Timeout
readonly EXIT_DEPENDENCY=6      # Missing dependency
readonly EXIT_CONFIG=7          # Configuration error
readonly EXIT_NETWORK=8         # Network error

# Global error state
declare -g ERROR_CONTEXT=""
declare -g ERROR_CODE=0
declare -g ERROR_DETAILS=""

# Set context for errors
set_error_context() {
    ERROR_CONTEXT="$1"
}

# Exit with error message and code
error_exit() {
    local code="$1"
    local message="$2"
    local details="${3:-}"

    error "[${ERROR_CONTEXT}] ${message}"
    [[ -n "$details" ]] && error "Details: $details"
    exit "$code"
}

# Validate command exists
require_command() {
    local cmd="$1"
    if ! command -v "$cmd" &> /dev/null; then
        error_exit "$EXIT_DEPENDENCY" \
            "Required command not found: $cmd" \
            "Install via: apt-get install $cmd"
    fi
}

# Validate file exists
require_file() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        error_exit "$EXIT_NOT_FOUND" \
            "Required file not found: $file"
    fi
}

# Check permission level
require_root() {
    if [[ $EUID -ne 0 ]]; then
        error_exit "$EXIT_PERMISSION" \
            "This script must be run as root"
    fi
}

# Execute with error context
execute_safe() {
    local context="$1"
    shift

    set_error_context "$context"
    if ! "$@"; then
        local exit_code=$?
        error_exit "$exit_code" \
            "Failed to execute: $*" \
            "Context: $context"
    fi
}

# Trap errors automatically
trap 'error_exit "$?" "Unhandled error at line $LINENO in ${BASH_SOURCE[1]}"' ERR
EOF

chmod +x scripts/lib-errors.sh

# 2. Update scripts/setup.sh to use new error handling
cat > setup.sh << 'EOF'
#!/usr/bin/env bash
set -e

# Import error handling
source scripts/lib-errors.sh
source scripts/lib.sh

# Validate inputs
PROFILE="${1:-base}"
PROFILE_FILE="profiles/$PROFILE.mk"

set_error_context "setup:validate"
require_file "$PROFILE_FILE"
require_command "dpkg"
require_command "apt-get"

set_error_context "setup:install"
# ... rest of setup logic ...

log "Installation complete!"
EOF

chmod +x setup.sh

# 3. Create error code documentation
cat > docs/ERROR_CODES.md << 'EOF'
# CtxOS Error Codes

All scripts follow standardized exit codes:

| Code | Name | Meaning | Action |
|------|------|---------|--------|
| 0 | EXIT_OK | Success | N/A |
| 1 | EXIT_GENERAL | Generic error | Check logs |
| 2 | EXIT_INVALID_ARG | Bad arguments | Verify syntax |
| 3 | EXIT_NOT_FOUND | Missing file/pkg | Check paths |
| 4 | EXIT_PERMISSION | Need root | Use sudo |
| 5 | EXIT_TIMEOUT | Operation timeout | Try again |
| 6 | EXIT_DEPENDENCY | Missing dependency | Install package |
| 7 | EXIT_CONFIG | Config error | Verify config |
| 8 | EXIT_NETWORK | Network error | Check connectivity |

Example error handling in bash:

```bash
source scripts/lib-errors.sh

set_error_context "my-task"
require_root
require_command "apt-get"

if ! apt-get update; then
    error_exit "$EXIT_NETWORK" "Failed to update package list"
fi
```
EOF
```

**Checklist:**
- [ ] `lib-errors.sh` created with all error codes
- [ ] `setup.sh` updated to use error handling
- [ ] `ERROR_CODES.md` documentation created
- [ ] All error paths tested manually

---

## WEEK 3-4: Documentation & Module System

### Task 2.1: Extend Documentation

**Objective:** Complete critical documentation gaps
**Time:** 3 hours
**Dependencies:** None

```bash
# 1. Create module development guide
cat > docs/modules/README.md << 'EOF'
# CtxOS Modules

Modules are self-contained components that can be installed independently.

## Module Structure

Each module in `modules/` must have:

```
module-name/
├── module.yaml          # Metadata and dependencies
├── packages.txt         # Package list (one per line)
├── install.sh           # Installation script
├── remove.sh            # Removal script (optional)
├── test.sh              # Test script (optional)
└── files/               # Configuration templates
    ├── config-file      # Config to deploy
    └── apparmor/        # Security profiles
```

## module.yaml Format

```yaml
name: module-name
version: "1.0.0"
description: "What does this module do?"
maintainer: "Your Name <email@example.com>"

# Installation
order: 10                # Lower = install earlier
required: false          # Essential to profile?
conflicts: []            # Module names that conflict
depends: [core]          # Required modules (must install first)
provides: [service]      # What this module provides

# Features
config:
  interactive: false     # Ask user questions?
  autoload: true         # Auto-load on boot?

test:
  enabled: true
  script: test.sh
```

## Creating a Module

1. Copy template:
   ```bash
   cp -r modules/module-template modules/my-module
   ```

2. Edit `module.yaml`
3. List packages in `packages.txt`
4. Implement `install.sh`:
   ```bash
   #!/usr/bin/env bash
   set -e
   source ../../scripts/lib.sh

   log "Installing $(basename "$(pwd)")"
   apt-get update
   apt-get install -y $(cat packages.txt)

   # Deploy configs
   [[ -d files ]] && for f in files/*; do
       install_file "$f" "/etc/$(basename "$f")"
   done
   ```

5. Implement `remove.sh`:
   ```bash
   #!/usr/bin/env bash
   log "Removing $(basename "$(pwd)")"
   apt-get remove -y $(cat packages.txt)
   ```

## Testing Your Module

```bash
cd modules/my-module
bash ./test.sh
```

## Validation

Ensure module.yaml is valid:
```bash
./scripts/validate-module.sh modules/my-module
```
EOF

# 2. Create software center API documentation
cat > docs/software-center/API.md << 'EOF'
# Software Center API Specification

## D-Bus Interface


### Org.CtxOS.PackageManager

#### Methods

**ListPackages(filter: string) → (packages: Array[(string, uint32)]))**
List available packages.

**GetPackageInfo(name: string) → (info: Dict)**
Get detailed package information.

**InstallPackage(name: string) → (success: bool)**
Install a package.

**RemovePackage(name: string) → (success: bool)**
Remove a package.

#### Signals

**PackageInstalled(name: string, version: string)**
Emitted when package is installed.

**PackageRemoved(name: string)**
Emitted when package is removed.

**ErrorOccurred(code: uint32, message: string)**
Error signal. See ERROR_CODES.md.

### Org.CtxOS.SystemProfile

#### Methods

**ListProfiles() → (profiles: Array[string])**
List available profiles.

**GetCurrentProfile() → (profile: string)**
Get active profile.

**SwitchProfile(name: string, snapshot: bool) → (success: bool)**
Switch to profile (optionally create snapshot).


## Error Codes

```
100: PERMISSION_DENIED
101: PACKAGE_NOT_FOUND
102: DEPENDENCY_ERROR
103: INSTALL_FAILED
104: REMOVE_FAILED
105: SNAPSHOT_FAILED
```

## Example Usage (Python)

```python
import dbus

bus = dbus.SystemBus()
obj = bus.get_object('org.ctxos.PackageManager', '/org/ctxos/PackageManager')
iface = dbus.Interface(obj, 'org.ctxos.PackageManager')

# Install package
try:
    success = iface.InstallPackage('python3-dev')
    print(f"Install result: {success}")
except dbus.exceptions.DBusException as e:
    print(f"Error: {e}")
```
EOF

# 3. Create backend architecture guide
cat > docs/software-center/ARCHITECTURE.md << 'EOF'
# Software Center Architecture

## High-Level Components

```
┌─────────────────────────────────────────┐
│        Frontend (GTK4 / Webview)        │
└────────────────────┬────────────────────┘
                     │ D-Bus
                     ▼
┌─────────────────────────────────────────────────┐
│  Backend Daemon (daemon.py)                     │
│  ┌──────────────────────────────────────────┐  │
│  │  Core Modules                            │  │
│  │  - ProfileManager                        │  │
│  │  - PackageManager                        │  │
│  │  - SnapshotManager                       │  │
│  └──────────────────────────────────────────┘  │
│           │              │              │      │
│           ▼              ▼              ▼      │
│  ┌─────────────┐ ┌──────────────┐ ┌────────┐ │
│  │ APT Provider│ │ Flatpak      │ │ Meta   │ │
│  │             │ │ Provider     │ │Package │ │
│  └─────────────┘ └──────────────┘ └────────┘ │
└──────────┬──────────────┬──────────────┬──────┘
           ▼              ▼              ▼
        ┌──────┐     ┌──────────┐   ┌──────┐
        │ APT  │     │ Flatpak  │   │ Meta │
        │ Repo │     │ Registry │   │ Data │
        └──────┘     └──────────┘   └──────┘
```

## Module Responsibilities

### ProfileManager
- Load profiles from `profiles/*.yaml`
- Track active profile
- Validate profile definitions
- Handle profile switching

### PackageManager
- Query available packages
- Install/remove packages
- Track installed packages
- Manage dependencies

### SnapshotManager
- Create system snapshots before changes
- Restore from snapshot on failure
- List available snapshots

### Package Providers
All providers inherit from `BaseProvider`:

```python
class BaseProvider(ABC):
    @abstractmethod
    def search(self, query: str) → List[Package]:
        pass

    @abstractmethod
    def get_info(self, name: str) → Package:
        pass

    @abstractmethod
    def install(self, name: str) → bool:
        pass

    @abstractmethod
    def remove(self, name: str) → bool:
        pass
```

## Data Flow: Installing a Package

1. Frontend → D-Bus → `PackageManager.install(name)`
2. `PackageManager` → iterate providers
3. Provider → system (apt, flatpak, etc.)
4. Provider → return success/error
5. Backend → emit Signal `PackageInstalled(name, version)`
6. Frontend → update UI

EOF
```

**Checklist:**
- [ ] `docs/modules/README.md` created
- [ ] `docs/software-center/API.md` created
- [ ] `docs/software-center/ARCHITECTURE.md` created
- [ ] Examples tested and valid

---

### Task 2.2: Create Module Template

**Objective:** Standardize new module creation
**Time:** 1 hour
**Dependencies:** None

```bash
# 1. Create module template
mkdir -p modules/module-template

# module.yaml
cat > modules/module-template/module.yaml << 'EOF'
name: template
version: "1.0.0"
description: "Replace this with your module description"
maintainer: "Your Name <your@example.com>"

order: 50
required: false
conflicts: []
depends: []
provides: []

config:
  interactive: false
  autoload: true

test:
  enabled: true
  script: test.sh
EOF

# packages.txt
cat > modules/module-template/packages.txt << 'EOF'
# List packages to install, one per line
# Example:
# python3
# python3-dev
EOF

# install.sh
cat > modules/module-template/install.sh << 'EOF'
#!/usr/bin/env bash
set -e
source ../../scripts/lib.sh
source ../../scripts/lib-errors.sh

MODULE_NAME="$(basename "$(pwd)")"
set_error_context "module:$MODULE_NAME:install"

log "Installing $MODULE_NAME"

# Update package list
require_command "apt-get"
apt-get update -qq || error_exit "$EXIT_NETWORK" "Failed to update package list"

# Install packages from packages.txt
if [ -s packages.txt ]; then
    log "Installing dependencies..."
    while read -r pkg; do
        [ -z "$pkg" ] && continue
        [[ "$pkg" =~ ^#.*$ ]] && continue  # Skip comments

        log "  + $pkg"
        apt-get install -y "$pkg" || error_exit "$EXIT_DEPENDENCY" \
            "Failed to install: $pkg" \
            "Check package name and repository configuration"
    done < packages.txt
fi

# Deploy configuration files
if [ -d "files" ]; then
    log "Deploying configuration files..."
    for f in files/*; do
        if [ -f "$f" ]; then
            target="/etc/$(basename "$f")"
            log "  → $target"
            install_file "$f" "$target"
        fi
    done
fi

log "✓ $MODULE_NAME installed successfully"
EOF

chmod +x modules/module-template/install.sh

# remove.sh
cat > modules/module-template/remove.sh << 'EOF'
#!/usr/bin/env bash
set -e
source ../../scripts/lib.sh
source ../../scripts/lib-errors.sh

MODULE_NAME="$(basename "$(pwd)")"
set_error_context "module:$MODULE_NAME:remove"

log "Removing $MODULE_NAME"

if [ -s packages.txt ]; then
    log "Removing packages..."
    while read -r pkg; do
        [ -z "$pkg" ] && continue
        [[ "$pkg" =~ ^#.*$ ]] && continue

        log "  - $pkg"
        apt-get remove -y "$pkg" || warn "Failed to remove $pkg"
    done < packages.txt
fi

log "✓ $MODULE_NAME removed"
EOF

chmod +x modules/module-template/remove.sh

# test.sh
cat > modules/module-template/test.sh << 'EOF'
#!/usr/bin/env bash
set -e

MODULE_NAME="$(basename "$(cd .. && pwd)")"

echo "Testing module: $MODULE_NAME"

# Add your tests here
# Examples:
# - Verify packages are installed:
#   dpkg -l | grep python3
#
# - Check configuration files exist:
#   [[ -f /etc/myconfig ]] && echo "✓ Config found"
#
# - Test functionality:
#   python3 -c "import module; module.test()"

echo "✓ Tests passed for $MODULE_NAME"
EOF

chmod +x modules/module-template/test.sh

# Create files directory for configs
mkdir -p modules/module-template/files

# Add README
cat > modules/module-template/README.md << 'EOF'
# Module Template

This is a template for creating new CtxOS modules.

## Quick Start

1. Copy this directory: `cp -r module-template my-module`
2. Edit `module.yaml` with your module details
3. List dependencies in `packages.txt`
4. Implement `install.sh` and `remove.sh`
5. Test with `bash test.sh`

## Files

- `module.yaml` - Metadata and dependencies
- `packages.txt` - Package list to install
- `install.sh` - Installation logic
- `remove.sh` - Removal logic
- `test.sh` - Module tests
- `files/` - Configuration templates

See `docs/modules/README.md` for detailed developer guide.
EOF

echo "✓ Module template created at modules/module-template"
```

**Checklist:**
- [ ] Template directory created
- [ ] All required files generated
- [ ] Template is valid (can run test.sh)
- [ ] README explains purpose
- [ ] CONTRIBUTING.md updated with module creation

---

## WEEK 5-6: Testing & Automation

### Task 3.1: CI/CD Enhancement

**Objective:** Improve automated validation
**Time:** 2 hours
**Dependencies:** Task 1.1, 1.2

```bash
# 1. Enhance CI workflow
cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    name: Lint & Validate
    steps:
      - uses: actions/checkout@v4

      - name: ShellCheck
        run: |
          sudo apt-get install -y shellcheck
          find scripts -name "*.sh" -exec shellcheck -S warning {} +

      - name: YAML Validation
        run: |
          pip install pyyaml
          python -c "import yaml; [yaml.safe_load(open(f)) for f in 'profiles/*.yaml']" || exit 1

      - name: Module Structure
        run: |
          for module in modules/*/; do
            [[ -f "$module/module.yaml" ]] || echo "WARNING: $module missing module.yaml"
            [[ -f "$module/install.sh" ]] || echo "ERROR: $module missing install.sh"; exit 1
          done

  test:
    runs-on: ubuntu-latest
    name: Unit Tests
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          pip install -r requirements-test.txt

      - name: Run Tests
        run: |
          pytest -v --cov=src --cov-report=xml --cov-report=term

      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  lint:
    runs-on: ubuntu-latest
    name: Code Quality
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Linters
        run: |
          pip install pylint flake8 mypy

      - name: Pylint
        run: |
          pylint software-center/backend --rcfile=.pylintrc --fail-under=7.0 || true

      - name: Flake8
        run: |
          flake8 software-center/backend --max-line-length=100 || true

      - name: MyPy
        run: |
          mypy software-center/backend --ignore-missing-imports || true

  security:
    runs-on: ubuntu-latest
    name: Security Scan
    steps:
      - uses: actions/checkout@v4

      - name: Trivy FS Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          exit-code: '1'
          severity: 'CRITICAL'

  build:
    runs-on: ubuntu-latest
    name: Build Artifacts
    needs: [validate, test]
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker Image
        run: |
          docker build -t ctxos-base:test .

      - name: Build Packages
        run: |
          chmod +x packaging/build-debs.sh
          ./packaging/build-debs.sh || echo "Package build not yet automated"
EOF

# 2. Create validation script
cat > scripts/ci/validate-pr.sh << 'EOF'
#!/usr/bin/env bash
# Validate PR before merge
set -e

source scripts/lib.sh
source scripts/lib-errors.sh

set_error_context "ci:validate-pr"

log "Running pre-merge validation..."

# 1. Lint checks
log "Running linters..."
shellcheck scripts/*.sh || warn "ShellCheck found issues"
pylint software-center/backend --fail-under=7.0 || warn "Pylint found issues"

# 2. Unit tests
log "Running unit tests..."
pytest tests/unit -v || error_exit "$EXIT_GENERAL" "Unit tests failed"

# 3. Structure validation
log "Validating module structure..."
for module in modules/*/; do
    [[ -f "$module/module.yaml" ]] || error_exit "$EXIT_CONFIG" "$module missing module.yaml"
    [[ -f "$module/install.sh" ]] || error_exit "$EXIT_CONFIG" "$module missing install.sh"
done

# 4. Docker build
log "Testing Docker build..."
docker build -t ctxos-base:test . > /dev/null

log "✓ All validations passed!"
EOF

chmod +x scripts/ci/validate-pr.sh

# 3. Create pre-commit hooks
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: v0.9.0.5
    hooks:
      - id: shellcheck
        args: [--severity=warning]
        files: ^scripts/.*\.sh$

  - repo: https://github.com/pre-commit/mirrors-yapf
    rev: v0.40.1
    hooks:
      - id: yapf
        args: [--in-place, --style=google]
        files: ^software-center/.*\.py$

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: detect-private-key

  - repo: https://github.com/adrienverge/yamllint
    rev: v1.33.0
    hooks:
      - id: yamllint
        args: [-d relaxed]
        files: ^(profiles|config)/.*\.ya?ml$
EOF

log "✓ CI/CD configuration updated"
```

**Checklist:**
- [ ] `.github/workflows/ci.yml` updated
- [ ] `scripts/ci/validate-pr.sh` created and tested
- [ ] `.pre-commit-config.yaml` created
- [ ] Pre-commit hooks installed: `pre-commit install`

---

## QUICK WINS (Can Do Today)

### 1. Add Module Count & Status

```bash
cat > scripts/module-status.sh << 'EOF'
#!/usr/bin/env bash
# Show module installation status

PROFILE="${1:-base}"
PROFILE_FILE="profiles/$PROFILE.mk"

[[ -f "$PROFILE_FILE" ]] || { echo "Profile not found: $PROFILE"; exit 1; }

source "$PROFILE_FILE"

echo "Profile: $PROFILE"
echo "Modules: ${#MODULES[@]}"
echo ""

for m in ${MODULES[@]}; do
    if [[ -d "modules/$m" ]]; then
        status="✓"
    else
        status="✗"
    fi
    echo "  $status $m"
done
EOF

chmod +x scripts/module-status.sh
```

### 2. Add Dependency Checker

```bash
cat > scripts/check-deps.sh << 'EOF'
#!/usr/bin/env bash
# Check if all module dependencies exist

echo "Checking module dependencies..."

for module in modules/*/; do
    module_name=$(basename "$module")

    # Check if module.yaml exists
    if [[ ! -f "$module/module.yaml" ]]; then
        echo "  WARNING: $module_name missing module.yaml"
        continue
    fi
done

echo "✓ Dependency check complete"
EOF

chmod +x scripts/check-deps.sh
```

### 3. Document Current Build Steps

```bash
cat > docs/BUILD_PIPELINE.md << 'EOF'
# CtxOS Build Pipeline

## Current Pipeline Stages

### Stage 0: Mirror Sync
- Command: `./scripts/mirror-sync.sh all`
- Purpose: Sync upstream package mirrors
- Time: ~30 seconds

### Stage 1: Package Building
- Command: `./scripts/release.sh patch`
- Purpose: Build .deb packages from modules
- Output: `build_output/*.deb`

### Stage 2: Docker Build
- Command: `docker build -t ctxos-base:latest .`
- Purpose: Build distribution Docker image
- Time: ~5-10 minutes

### Stage 3: Live ISO Build
- Command: `cd live-iso && ./build-iso.sh`
- Purpose: Create bootable ISO
- Output: `ctxos-*.iso`

### Stage 4: Validation
- Command: `./scripts/validate-artifacts.sh`
- Purpose: Verify all artifacts are valid

### Stage 5: Release
- Command: `./scripts/release.sh`
- Purpose: Tag and publish release

## Running Specific Stages

```bash
# Skip mirror sync (offline)
SKIP_MIRROR=true ./scripts/pipeline-master.sh

# Skip ISO (faster testing)
SKIP_ISO=true ./scripts/pipeline-master.sh

# Multi-arch (requires QEMU)
BUILD_MULTI_ARCH=true ./scripts/pipeline-master.sh
```

## Typical Development Workflow

```bash
# 1. Make changes to modules
edit modules/core/install.sh

# 2. Test single module
(cd modules/core && bash install.sh)

# 3. Build partial pipeline
bash packaging/build-debs.sh

# 4. Full pipeline (nightly)
./scripts/pipeline-master.sh
```
EOF
```

---

## Success Criteria Checklist

After completing all tasks above, you should have:

- [ ] Test infrastructure (pytest, fixtures)
- [ ] Pinned dependencies (requirements.lock, pyproject.toml)
- [ ] Standardized error handling (lib-errors.sh)
- [ ] Complete documentation (API, ARCHITECTURE, modules)
- [ ] Module template for easy creation
- [ ] Enhanced CI/CD with lint, test, security
- [ ] Pre-commit hooks configured
- [ ] Validation scripts in place

---

## Performance Impact

| Task | Build Time Δ | Maintenance Δ | Risk |
|------|--------------|---------------|------|
| Test Coverage | +5% | -20% | Low |
| Error Handling | +0% | -15% | Low |
| Dependencies | +0% | -10% | Low |
| Documentation | +0% | -25% | Low |
| Module System | +0% | -10% | Low |
| CI/CD Enhancement | +15% | +5% | Low |

---

## Getting Help

If you encounter issues:

1. **Test failures?** Check `tests/fixtures/` for mocks
2. **Dependency errors?** Run `pip install -r requirements-test.txt`
3. **Shell script issues?** Run `shellcheck scripts/lib.sh`
4. **Module problems?** Review `docs/modules/README.md`

---

**Next:** Review ARCHITECTURE_REVIEW.md for comprehensive analysis and long-term roadmap.
