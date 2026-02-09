PROFILE ?= base

.PHONY: all install uninstall iso debs clean help

all: install

install:
	@echo "▶ Installing profile: $(PROFILE)"
	@bash setup.sh $(PROFILE)

uninstall:
	@echo "▶ Uninstalling profile: $(PROFILE)"
	@bash uninstall.sh $(PROFILE)

module-%:
	@bash modules/$*/install.sh

iso:
	@bash live-iso/build-iso.sh

debs:
	@bash packaging/build-debs.sh

clean:
	@rm -rf build dist
	@find modules -name "*.log" -delete

help:
	@echo "Debian Base Kit Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install         Install all modules"
	@echo "  make uninstall       Uninstall all modules"
	@echo "  make module-<name>   Install a specific module"
	@echo "  make iso             Build live ISO"
	@echo "  make debs            Build .deb packages"
	@echo "  make clean           Clean build artifacts"
