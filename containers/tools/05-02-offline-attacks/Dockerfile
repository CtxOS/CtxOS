# CtxOS Tool Collection - • Offline Attacks
# Category: 05-02-offline-attacks
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Offline Attacks
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="hashcat john johnny" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
