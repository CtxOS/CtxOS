# CtxOS Tool Collection - • SMTP Analysis
# Category: 01-11-smtp-analysis
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • SMTP Analysis
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="swaks" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
