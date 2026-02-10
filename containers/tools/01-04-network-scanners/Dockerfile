# CtxOS Tool Collection - • Network Scanners
# Category: 01-04-network-scanners
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Network Scanners
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="amap nmap nmapsi4 nmapsi4-root" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
