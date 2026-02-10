# CtxOS Tool Collection - 13 - Automotive
# Category: 13-automotive
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for 13 - Automotive
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="can-calc-bit-timing canbus-triple canbusload candump canfdtest cangen cangw canlogserver canplayer cansend caring-caribou slcan-attach slcand slcanpty" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
