# CtxOS Tool Collection - 05 - Password Attacks
# Category: 05-password-attacks
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for 05 - Password Attacks
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="crackle crunch fcrackzip findmyhash hash-identifier hashcat hashdeep hashid hashrat hydra john johnny medusa mimikatz ncrack ophcrack-cli passing-the-hash pdfcrack rahash2 rainbowcrack rarcrack rcrack rcracki-mt rcracki_mt rizin-hash sipcrack sucrack svcrack truecrack xhydra" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
