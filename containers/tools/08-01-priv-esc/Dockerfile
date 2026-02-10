# CtxOS Tool Collection - • Privilege Escalation
# Category: 08-01-priv-esc
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Privilege Escalation
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="peass unix-privesc-check" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
