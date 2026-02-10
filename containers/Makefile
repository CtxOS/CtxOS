# CtxOS Container Images Makefile

VERSION ?= $(shell cat ../VERSION 2>/dev/null || echo "latest")
IMAGE_PREFIX = ctxos

.PHONY: all core security tools clean help

all: core security tools

help:
	@echo "CtxOS Container Build System"
	@echo ""
	@echo "Usage:"
	@echo "  make core       - Build the foundation image"
	@echo "  make security   - Build the comprehensive security toolkit"
	@echo "  make tools      - Build all individual tool images"
	@echo "  make all        - Build everything (order: core -> security -> tools)"
	@echo "  make clean      - Remove built images"

core:
	docker build -t $(IMAGE_PREFIX)/core:$(VERSION) -t $(IMAGE_PREFIX)/core:latest ./core

security: core
	docker build -t $(IMAGE_PREFIX)/security:$(VERSION) -t $(IMAGE_PREFIX)/security:latest ./security

tools: nmap masscan gobuster sqlmap

nmap: core
	docker build -t $(IMAGE_PREFIX)/tool-nmap:$(VERSION) -t $(IMAGE_PREFIX)/tool-nmap:latest ./tools/nmap

masscan: core
	docker build -t $(IMAGE_PREFIX)/tool-masscan:$(VERSION) -t $(IMAGE_PREFIX)/tool-masscan:latest ./tools/masscan

gobuster: core
	docker build -t $(IMAGE_PREFIX)/tool-gobuster:$(VERSION) -t $(IMAGE_PREFIX)/tool-gobuster:latest ./tools/gobuster

sqlmap: core
	docker build -t $(IMAGE_PREFIX)/tool-sqlmap:$(VERSION) -t $(IMAGE_PREFIX)/tool-sqlmap:latest ./tools/sqlmap

clean:
	docker rmi $$(docker images -q "$(IMAGE_PREFIX)/*") || true
