# CtxOS Tool Collection - • Debuggers
# Category: 07-02-debuggers
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Debuggers
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="ollydbg" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
