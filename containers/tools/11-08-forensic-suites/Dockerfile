# CtxOS Tool Collection - • Forensic Suites
# Category: 11-08-forensic-suites
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Forensic Suites
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="autopsy" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
