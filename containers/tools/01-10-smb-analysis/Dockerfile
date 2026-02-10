# CtxOS Tool Collection - • SMB Analysis
# Category: 01-10-smb-analysis
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • SMB Analysis
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="enum4linux" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
