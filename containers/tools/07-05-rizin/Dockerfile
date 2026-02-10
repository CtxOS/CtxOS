# CtxOS Tool Collection - • Rizin
# Category: 07-05-rizin
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Rizin
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="rizin rizin-asm rizin-ax rizin-bin rizin-cutter rizin-diff rizin-find rizin-gg rizin-pm rizin-run" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
