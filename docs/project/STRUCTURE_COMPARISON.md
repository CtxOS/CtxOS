# CtxOS: Current vs. Proposed Structure

## Side-by-Side Comparison

### Current State (Feb 2026)

```
CtxOS/
├── Root Level
│   ├── Makefile              [Basic - limited targets]
│   ├── VERSION               [Plain text "1.0.1"]
│   ├── setup.sh              [Main installer]
│   ├── uninstall.sh
│   ├── requirements.txt       [Unpinned: pywebview>=5.0]
│   └── LICENSE
│
├── scripts/ (18 files)
│   ├── lib.sh               [Basic helpers]
│   ├── log.sh               [Simple colored output]
│   ├── pipeline-master.sh   [Monolithic 70+ lines]
│   ├── release.sh
│   ├── validate-artifacts.sh
│   ├── security-audit.sh
│   ├── docker-run.sh
│   ├── run-vm.sh            [VM testing]
│   ├── wsl-setup.sh
│   ├── mirror-sync.sh
│   ├── generate-metadata.sh
│   ├── project-packager.sh
│   └── ... 6 more utilities
│
├── modules/ (13 modules)
│   ├── core/
│   │   ├── packages.txt
│   │   ├── install.sh       [No module.yaml]
│   │   ├── remove.sh        [No versioning]
│   │   └── files/
│   ├── apt/
│   ├── firefox/
│   ├── interface/
│   ├── menu/
│   ├── themes/
│   ├── tools/
│   ├── updater/
│   ├── zsh-config/
│   └── ... (no dependency graph)
│
├── software-center/         [Main app]
│   ├── backend/
│   │   ├── daemon.py        [Monolithic entry point]
│   │   ├── api/             [Endpoints - undocumented]
│   │   ├── dbus/            [D-Bus service defs]
│   │   ├── providers/       [APT, Flatpak, Meta]
│   │   └── locales/
│   ├── frontend/
│   │   ├── gtk/             [GTK4 main.py]
│   │   └── web/             [HTML/CSS]
│   ├── assets/
│   ├── bin/
│   ├── debian/
│   ├── polkit/
│   ├── Makefile
│   ├── README.md
│   └── webview_launcher.py
│
├── workflow/                [Next.js visualizer]
│   ├── package.json         [dependencies: "latest"]
│   ├── pnpm-lock.yaml       [Good - locked]
│   ├── next.config.mjs
│   ├── app/
│   ├── components/
│   ├── .../
│   └── README.md
│
├── profiles/ (4 profiles)
│   ├── base.mk              [Makefile syntax - just lists]
│   ├── desktop.mk           [No structured metadata]
│   ├── server.mk            [No dependency info]
│   ├── rescue.mk            [No conflict info]
│   └── README.md            [Missing]
│
├── packaging/
│   ├── build-debs.sh        [Builds .deb packages]
│   ├── deb/
│   └── repo/
│
├── live-iso/
│   ├── build-iso.sh
│   ├── armbian-builder/
│   ├── prepare-custom-packages.sh
│   └── config/
│
├── containers/
│   ├── core/
│   ├── security/
│   ├── tools/
│   └── Makefile
│
├── docs/
│   ├── architecture.md       [40 lines - basic]
│   ├── live-iso.md
│   ├── packaging.md
│   └── recovery.md
│
├── .github/workflows/
│   ├── ci.yml               [ShellCheck only]
│   ├── software-center.yml
│   ├── production-pipeline.yml
│   └── deploy-pages.yml
│
├── config/                  [Live-build config]
├── recovery/                [Rescue tools]
├── projects/                [Project isolation]
├── mirror/                  [Mirror sync tools]
├── locales/                 [i18n data]
├── build_output/            [Build artifacts]
│
├── .gitignore
├── .vscode/
├── Dockerfile               [Root level]
├── Dockerfile.build
├── Dockerfile.test
├── index.html
├── style.css
├── main.js
│
├── CONTRIBUTING.md
├── README.md
├── SECURITY.md
└── branding.json

❌ Missing:
- No tests/ directory
- No pyproject.toml
- No pre-commit config
- No comprehensive docs
- No module.yaml formats
- No version management
- No API specification
- No error handling standards
- No dependency lock validation
- No module templates
```

---

### Proposed State (After Improvements)

```
CtxOS/
├── 📋 PROJECT METADATA       [IMPROVED]
│   ├── VERSION              [Enhanced: version management]
│   ├── pyproject.toml       [✨ NEW - Python packaging]
│   ├── requirements-prod.txt [✨ NEW - pinned versions]
│   ├── requirements-dev.txt  [✨ NEW - dev-only deps]
│   ├── requirements.lock    [✨ NEW - lock file]
│   ├── .editorconfig        [✨ NEW - coding standards]
│   ├── .pre-commit-config.yaml [✨ NEW - git hooks]
│   ├── ARCHITECTURE_REVIEW.md [✨ NEW - this analysis]
│   ├── IMPLEMENTATION_GUIDE.md [✨ NEW - how-to steps]
│   ├── PROJECT_REVIEW.md    [✨ NEW - executive summary]
│   ├── LICENSE              [Existing]
│   ├── README.md            [Existing]
│   ├── CONTRIBUTING.md      [Improved]
│   ├── SECURITY.md          [Existing]
│   └── Makefile             [Enhanced]
│
├── 📚 DOCUMENTATION          [✨ MAJOR EXPANSION]
│   ├── README.md            [Overview]
│   ├── GETTING_STARTED.md   [✨ NEW]
│   ├── ARCHITECTURE.md      [Expanded]
│   ├── BUILD_PIPELINE.md    [✨ NEW]
│   ├── ERROR_CODES.md       [✨ NEW - error reference]
│   ├── RELEASE.md           [✨ NEW - versioning strategy]
│   │
│   ├── backend/             [✨ NEW FOLDER]
│   │   ├── README.md
│   │   ├── ARCHITECTURE.md  [Backend design details]
│   │   ├── API.md           [✨ NEW - D-Bus interface spec]
│   │   ├── API_SPECIFICATION.md [✨ NEW - formal spec]
│   │   ├── PROVIDERS.md     [✨ NEW - provider interface]
│   │   └── ERROR_CODES.md
│   │
│   ├── modules/             [✨ NEW FOLDER]
│   │   ├── README.md        [✨ NEW - module guide]
│   │   ├── DEVELOPING.md    [✨ NEW - dev guidelines]
│   │   └── MODULE_TEMPLATE/ [✨ NEW - starter template]
│   │
│   ├── workflow/            [✨ NEW FOLDER]
│   │   ├── CI_CD.md         [✨ NEW - CI/CD reference]
│   │   └── RELEASE_PROCESS.md [✨ NEW - release guide]
│   │
│   └── architecture-diagrams/ [✨ NEW]
│       ├── component-map.md
│       ├── data-flow.md
│       └── deployment.md
│
├── 🧪 TESTS                 [✨ ENTIRE NEW SECTION]
│   ├── conftest.py          [✨ NEW - pytest fixtures]
│   ├── pytest.ini           [✨ NEW - pytest config]
│   │
│   ├── unit/                [✨ NEW - unit tests]
│   │   ├── test_package_providers.py
│   │   ├── test_profile_manager.py
│   │   ├── test_version_manager.py
│   │   ├── test_deployment.py
│   │   └── __init__.py
│   │
│   ├── integration/         [✨ NEW - integration tests]
│   │   ├── test_module_install.sh
│   │   ├── test_iso_build.sh
│   │   └── test_docker_build.sh
│   │
│   ├── e2e/                 [✨ NEW - end-to-end tests]
│   │   ├── test_full_pipeline.sh
│   │   └── test_profile_switch.sh
│   │
│   ├── fixtures/            [✨ NEW - test data]
│   │   ├── mock_apt_cache.py
│   │   ├── test_profiles.mk
│   │   └── sample_modules/
│   │
│   └── benchmarks/          [✨ NEW - performance]
│       └── package_discovery.py
│
├── 📦 SOURCE CODE STRUCTURE [REORGANIZED]
│   ├── src/                 [✨ NEW - root source folder]
│   │
│   ├── backend/             [✨ MOVED from software-center]
│   │   ├── __init__.py
│   │   ├── daemon.py        [Modularized entry point]
│   │   ├── api/             [EXPANDED endpoints]
│   │   │   ├── __init__.py
│   │   │   ├── packages.py
│   │   │   ├── profiles.py
│   │   │   ├── system.py
│   │   │   └── middleware.py [✨ NEW]
│   │   │
│   │   ├── core/            [✨ NEW - business logic]
│   │   │   ├── __init__.py
│   │   │   ├── package_manager.py
│   │   │   ├── profile_manager.py [✨ refactored]
│   │   │   ├── snapshot_manager.py
│   │   │   └── version_manager.py [✨ NEW]
│   │   │
│   │   ├── providers/       [IMPROVED]
│   │   │   ├── __init__.py
│   │   │   ├── base.py      [✨ NEW - abstract class]
│   │   │   ├── apt_provider.py
│   │   │   ├── flatpak_provider.py
│   │   │   └── meta_provider.py
│   │   │
│   │   ├── dbus/            [SAME]
│   │   │   ├── __init__.py
│   │   │   └── service.py
│   │   │
│   │   ├── models/          [✨ NEW - data models]
│   │   │   ├── __init__.py
│   │   │   ├── package.py
│   │   │   ├── profile.py
│   │   │   └── error.py
│   │   │
│   │   ├── errors.py        [✨ NEW - custom exceptions]
│   │   ├── config.py        [✨ NEW - config mgmt]
│   │   ├── logger.py        [✨ NEW - structured logging]
│   │   ├── py.typed         [✨ NEW - PEP 561]
│   │   └── locales/         [SAME]
│   │
│   ├── cli/                 [✨ NEW - command-line]
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── commands/
│   │   │   ├── build.py
│   │   │   ├── install.py
│   │   │   └── validate.py
│   │   └── shell-completions/
│   │
│   ├── frontend/
│   │   ├── gtk/             [SAME]
│   │   │   ├── main.py
│   │   │   ├── windows/
│   │   │   └── widgets/
│   │   └── web/             [SAME]
│   │
│   └── scripts/             [REORGANIZED]
│       ├── lib/             [✨ STRUCTURED]
│       │   ├── lib-core.sh
│       │   ├── lib-errors.sh [✨ NEW - error codes]
│       │   ├── lib-validation.sh [✨ NEW]
│       │   ├── lib-logging.sh [✨ NEW]
│       │   └── lib-packaging.sh
│       │
│       ├── install/         [✨ ORGANIZED]
│       │   ├── setup.sh
│       │   └── uninstall.sh
│       │
│       ├── build/           [✨ ORGANIZED]
│       │   ├── pipeline.sh
│       │   ├── build-debs.sh
│       │   └── build-iso.sh
│       │
│       ├── tools/           [✨ ORGANIZED]
│       │   ├── mirror-sync.sh
│       │   ├── validate-artifacts.sh
│       │   ├── security-audit.sh
│       │   ├── release.sh
│       │   └── generate-metadata.sh
│       │
│       ├── ci/              [✨ NEW - CI/CD scripts]
│       │   ├── lint-check.sh [✨ NEW]
│       │   ├── test-runner.sh [✨ NEW]
│       │   └── validate-pr.sh [✨ NEW]
│       │
│       └── dev/             [✨ ORGANIZED]
│           ├── docker-run.sh
│           ├── run-vm.sh
│           └── wsl-setup.sh
│
├── 🏗️ INFRASTRUCTURE        [IMPROVED]
│   ├── docker/              [✨ NEW - standalone folder]
│   │   ├── Dockerfile       [MOVED from root]
│   │   ├── Dockerfile.build [MOVED]
│   │   └── docker-compose.yml [✨ NEW]
│   │
│   ├── containers/          [SAME - tools]
│   │   ├── core/
│   │   ├── security/
│   │   └── tools/
│   │
│   ├── live-iso/            [SAME]
│   │
│   ├── kubernetes/          [✨ NEW - future use]
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   │
│   └── terraform/           [✨ NEW - future use]
│       └── main.tf
│
├── 🧩 MODULES              [IMPROVED]
│   ├── README.md            [✨ NEW - module guide]
│   │
│   ├── module-template/     [✨ NEW - starter template]
│   │   ├── module.yaml      [✨ NEW - structured]
│   │   ├── packages.txt
│   │   ├── install.sh
│   │   ├── remove.sh
│   │   ├── test.sh          [✨ NEW]
│   │   └── files/
│   │
│   ├── core/
│   │   ├── module.yaml      [✨ NEW - metadata]
│   │   ├── packages.txt     [Same]
│   │   ├── install.sh
│   │   ├── remove.sh
│   │   └── files/
│   │
│   ├── apt/                 [✨ Add module.yaml]
│   ├── firefox/             [✨ Add module.yaml]
│   ├── interface/           [✨ Add module.yaml]
│   ├── menu/                [✨ Add module.yaml]
│   ├── themes/              [✨ Add module.yaml]
│   ├── tools/               [✨ Add module.yaml]
│   ├── updater/             [✨ Add module.yaml]
│   └── zsh-config/          [✨ Add module.yaml]
│
├── 📋 PROFILES             [IMPROVED]
│   ├── README.md            [✨ NEW - profile guide]
│   │
│   ├── base.yaml            [✨ NEW - YAML format]
│   │   # Convert from base.mk
│   │   name: base
│   │   modules:
│   │     apt: {order: 1}
│   │     core: {order: 2}
│   │
│   ├── desktop.yaml         [✨ NEW]
│   ├── server.yaml          [✨ NEW]
│   ├── rescue.yaml          [✨ NEW]
│   │
│   └── validator/           [✨ NEW]
│       └── validate-profile.sh
│
├── 🔧 CONFIGURATION        [SAME]
│   ├── README.md            [✨ NEW]
│   ├── templates/           [Live-build templates]
│   ├── presets/             [✨ NEW - config presets]
│   │   ├── minimal.yaml
│   │   ├── workstation.yaml
│   │   └── server.yaml
│   └── [live-build configs]
│
├── 📦 BUILD & PACKAGING    [SAME]
│   ├── packaging/           [Debian meta-packages]
│   ├── projects/            [Project isolation]
│   └── build_output/        [Build artifacts]
│
├── 🔄 CI/CD IMPROVEMENTS   [EXPANDED]
│   ├── .github/
│   │   ├── workflows/       [EXPANDED]
│   │   │   ├── ci.yml       [✨ ENHANCED - tests, lint, coverage]
│   │   │   ├── cd.yml       [✨ NEW - deployment pipeline]
│   │   │   ├── security.yml [✨ NEW - SAST, SBOM, scanning]
│   │   │   ├── performance.yml [✨ NEW - build metrics]
│   │   │   └── release.yml  [✨ NEW - release automation]
│   │   │
│   │   ├── actions/         [✨ NEW - reusable actions]
│   │   │   ├── setup-env.yml
│   │   │   ├── run-tests.yml
│   │   │   └── validate-artifacts.yml
│   │   │
│   │   └── CODEOWNERS       [✨ NEW - PR routing]
│   │
│   └── .pre-commit-config.yaml [✨ NEW - git hooks]
│
├── 📊 WORKFLOW (Existing)  [CAN BE DECOUPLED]
│   ├── package.json         [✨ ENHANCED - no "latest"]
│   ├── pnpm-lock.yaml       [SAME]
│   ├── README.md            [SAME]
│   ├── app/                 [SAME]
│   ├── components/          [SAME]
│   └── ...
│
├── 🔐 SECURITY & VERSIONING [✨ NEW ORGANIZATION]
│   ├── .lock/               [✨ NEW - dependency locks]
│   │   ├── requirements.lock
│   │   └── dependencies.txt [Shell package versions]
│   │
│   ├── version/             [✨ NEW - version management]
│   │   ├── VERSION
│   │   ├── CHANGELOG.md
│   │   └── bump.sh
│   │
│   └── .gitignore           [IMPROVED]
│
└── 📁 EXISTING (UNCHANGED)
    ├── config/              [Live-build configs]
    ├── recovery/            [Rescue tools]
    ├── projects/            [Project isolation]
    ├── mirror/              [Mirror sync]
    ├── locales/             [i18n data]
    ├── build_output/        [Build artifacts]
    ├── .git/
    └── local/               [Local functions]

✨ = NEW OR SIGNIFICANTLY IMPROVED
```

---

## Key Differences Highlighted

### Before (Issues) → After (Fixed)

| Area | Before | After |
|------|--------|-------|
| **Dependencies** | `pywebview>=5.0` (loose) | `pywebview==5.1.3` (pinned) |
| **Versioning** | Manual, text file | Automated with semver |
| **Tests** | None | 70+ test cases |
| **Module Definition** | Plain lists | Structured YAML with metadata |
| **Error Handling** | Inconsistent patterns | Standardized with error codes |
| **Documentation** | 100 lines | 2000+ lines across 20 docs |
| **CI/CD** | Linting only | Tests, lint, security, coverage |
| **API Spec** | Undocumented | Full OpenAPI specification |
| **Module Template** | None | Complete starter template |
| **Backend Code** | Monolithic daemon.py | Modularized with clear layers |

---

## Migration Path (Non-Breaking)

The proposed structure is **additive** - you don't need to remove anything:

### Week 1-2
```
Add:  tests/, pyproject.toml, requirements-*.txt
Keep: All existing scripts and configs working
```

### Week 3-4
```
Add:  docs/*, module-template/
Keep: Existing modules still work without module.yaml
```

### Week 5-6
```
Add:  Enhanced CI/CD workflows
Keep: Old pipeline still runs
```

### Future (with deprecation period)
```
Convert: profiles/*.mk → profiles/*.yaml (6-month deprecation)
Migrate: software-center/backend → src/backend (with compatibility layer)
```

---

## File Impact Summary

```
Total Files to ADD:     ~80 new files
  - Tests (20 files)
  - Documentation (30 files)
  - Configuration (10 files)
  - Source refactoring (20 files)

Total Files to MODIFY:  ~15 existing files
  - scripts/ (reorganized into subdirs)
  - .github/workflows/ (enhanced)
  - pyproject.toml (new)
  - requirements*.txt (new)

Total Files to DELETE:  0 (none - backward compatible)

Total Lines of Code:    ~10,000 added
  - Tests: 3,000 lines
  - Docs: 4,000 lines
  - Code refactoring: 2,000 lines
  - Configuration: 1,000 lines
```

---

## Benefit Timeline

| Milestone | When | Benefit |
|-----------|------|---------|
| Tests in place | Week 1 | Can refactor safely |
| Deps pinned | Week 1 | Reproducible builds |
| Error handling std | Week 2 | User-friendly errors |
| Docs published | Week 3 | Faster onboarding |
| Module template | Week 3 | Faster development |
| CI/CD enhanced | Week 5 | Catch bugs early |
| **70% test coverage** | **Month 2** | **Enterprise ready** |

---

## Visual: The Transformation

```
Current State (7/10)          After Improvements (9/10)
─────────────────────────────────────────────────────

Scattered scripts      →      Organized by purpose
(20 files, unclear)            (organized in subdirs)

No tests              →      Comprehensive coverage
(0% coverage)                 (70%+ coverage)

Loose deps            →      Pinned versions
(">=5.0")                     ("==5.1.3")

No docs               →      Comprehensive docs
(100 lines)                   (2000+ lines)

Basic CI              →      Enterprise CI/CD
(ShellCheck only)             (tests, lint, security)

Implicit module deps  →      Explicit dependencies
(install order only)          (with validation)

Monolithic backends   →      Layered architecture
(big files)                   (clear separation)

Empirical errors      →      Documented error codes
("Something failed")          ("101: PACKAGE_NOT_FOUND")
```

---

## Conclusion

The proposed structure provides:

✅ **Maintainability** - Clear organization, easy to find code
✅ **Reliability** - Comprehensive tests catch regressions
✅ **Scalability** - Modular design supports growth
✅ **Professionalism** - Documentation and standards
✅ **Developer Experience** - Faster onboarding, better tools

**Status:** Ready to implement immediately
**Backward Compatible:** 100% - no breaking changes
**Estimated Implementation Time:** 6 weeks

Start with Task 1.1 in IMPLEMENTATION_GUIDE.md!
