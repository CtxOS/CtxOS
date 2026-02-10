# CtxOS Tool Collection - • Forensic Carving Tools
# Category: 11-05-forensic-carving-tools
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Forensic Carving Tools
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="foremost scalpel" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
