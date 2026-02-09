DESTDIR ?=
PREFIX ?= /usr

.PHONY: all install build-deb

all:
	@echo "Nothing to build. Use 'make install' or 'make build-deb'"

install:
	mkdir -p $(DESTDIR)$(PREFIX)/lib/software-center/backend
	mkdir -p $(DESTDIR)$(PREFIX)/lib/software-center/web
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	mkdir -p $(DESTDIR)/etc/dbus-1/system.d
	mkdir -p $(DESTDIR)/lib/systemd/system
	mkdir -p $(DESTDIR)$(PREFIX)/share/polkit-1/actions

	cp -r backend/* $(DESTDIR)$(PREFIX)/lib/software-center/backend/
	cp -r web/* $(DESTDIR)$(PREFIX)/lib/software-center/web/
	cp webview_launcher.py $(DESTDIR)$(PREFIX)/lib/software-center/
	cp frontend/gtk/main.py $(DESTDIR)$(PREFIX)/lib/software-center/main_gtk.py
	
	cp bin/software-center-gtk $(DESTDIR)$(PREFIX)/bin/
	cp bin/software-center-webview $(DESTDIR)$(PREFIX)/bin/
	
	cp backend/dbus/org.ctxos.SoftwareCenter.conf $(DESTDIR)/etc/dbus-1/system.d/
	cp backend/dbus/org.ctxos.SoftwareCenter.service $(DESTDIR)/lib/systemd/system/
	cp polkit/org.ctxos.softwarecenter.policy $(DESTDIR)$(PREFIX)/share/polkit-1/actions/

	chmod +x $(DESTDIR)$(PREFIX)/bin/software-center-gtk
	chmod +x $(DESTDIR)$(PREFIX)/bin/software-center-webview
	chmod +x $(DESTDIR)$(PREFIX)/lib/software-center/backend/daemon.py

build-deb:
	debuild -us -uc -b
