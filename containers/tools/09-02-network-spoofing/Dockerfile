# CtxOS Tool Collection - • Network Spoofing
# Category: 09-02-network-spoofing
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Network Spoofing
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="ettercap-graphical ettercap-text" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
