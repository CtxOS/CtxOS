# CtxOS Tool Collection - 09 - Sniffing & Spoofing
# Category: 09-sniffing-spoofing
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for 09 - Sniffing & Spoofing
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="cansniffer detect_sniffer6 dnsspoof dsniff ettercap-graphical ettercap-text isotpsniffer netsniff sniffjoke spooftooph sslsniff wireshark" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
