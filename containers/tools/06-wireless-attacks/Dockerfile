# CtxOS Tool Collection - 06 - Wireless Attacks
# Category: 06-wireless-attacks
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for 06 - Wireless Attacks
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="airbase aircrack-ng airdecap airdecloak aireplay airmon airodump airolib airserv airtun bluelog blueranger bluesnarfer btscanner bully fern-wifi-cracker nbtscan reaver sparrow-wifi wifi-honey" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
