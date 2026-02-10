# CtxOS Tool Collection - • Profile
# Category: 05-05-profile
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Profile
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="crunch" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
