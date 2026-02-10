# CtxOS Tool Collection - • Web Crawlers
# Category: 03-04-web-crawlers
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Web Crawlers
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="apache-users dirb gobuster" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
