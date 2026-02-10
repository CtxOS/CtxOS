# CtxOS Tool Collection - • DNS Analysis
# Category: 01-01-dns-analysis
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for • DNS Analysis
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="dns-rebind dns2tcpc dns2tcpd dnscat2-client dnscat2-server dnschef dnsdict6 dnsenum dnsmap dnsrecon dnstracer dnswalk fake_dns6d fake_dnsupdate6" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
