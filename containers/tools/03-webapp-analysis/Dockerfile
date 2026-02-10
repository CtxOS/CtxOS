# CtxOS Tool Collection - 03 - Web Application Analysis
# Category: 03-webapp-analysis
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for 03 - Web Application Analysis
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="burpsuite-legacy dirb gobuster jsql jsql-injection mdb-sql mitmproxy postgresql proxytunnel sqldict sqlitebrowser sqlmap sqlninja sqlsus webacoo webmitm webscarab webshells websploit webspy whatweb" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
