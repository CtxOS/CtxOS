# CtxOS Tool Collection - • Network Sniffers
# Category: 09-01-network-sniffers
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Network Sniffers
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="wireshark" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
