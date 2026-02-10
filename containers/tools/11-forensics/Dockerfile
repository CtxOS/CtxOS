# CtxOS Tool Collection - 11 - Forensics
# Category: 11-forensics
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for 11 - Forensics
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="autopsy foremost icat-sleuthkit ils-sleuthkit mactime-sleuthkit scalpel volatility3-vol volatility3-volshell" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
