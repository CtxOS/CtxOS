# CtxOS Tool Collection - • Fuzzers
# Category: 02-02-fuzzers
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • Fuzzers
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="spike spike-generic-chunked spike-generic-listen-tcp spike-generic-send-tcp spike-generic-send-udp" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
