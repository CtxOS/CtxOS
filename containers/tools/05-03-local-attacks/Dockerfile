# CtxOS Tool Collection - • Local Attacks
# Category: 05-03-local-attacks
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Local Attacks
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="mimikatz" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
