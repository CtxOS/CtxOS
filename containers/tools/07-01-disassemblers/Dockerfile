# CtxOS Tool Collection - • Disassemblers
# Category: 07-01-disassemblers
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Disassemblers
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="bddisasm" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
