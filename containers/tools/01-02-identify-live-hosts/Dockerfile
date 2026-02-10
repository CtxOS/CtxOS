# CtxOS Tool Collection - • Identify Live Hosts
# Category: 01-02-identify-live-hosts
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Identify Live Hosts
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="fping hping3" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
