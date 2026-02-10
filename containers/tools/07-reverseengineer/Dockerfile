# CtxOS Tool Collection - 07 - Reverse Engineering
# Category: 07-reverseengineer
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for 07 - Reverse Engineering
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="apktool bddisasm edb-debugger ghidra jadx jadx-gui javasnoop ollydbg rizin rizin-asm rizin-ax rizin-bin rizin-cutter rizin-diff rizin-find rizin-gg rizin-pm rizin-run" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
