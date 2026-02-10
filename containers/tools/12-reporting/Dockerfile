# CtxOS Tool Collection - 12 - Reporting Tools
# Category: 12-reporting
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for 12 - Reporting Tools
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="dradis" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
