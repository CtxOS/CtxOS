# CtxOS Core - Foundation for all CtxOS Container Images
FROM debian:bookworm-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    CTXOS_VERSION=1.0.0 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# Install base system utilities and locales
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    lsb-release \
    locales \
    wget \
    procps \
    vim-tiny \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*

# Add CtxOS Repository security key
COPY ctxos.asc /tmp/ctxos.asc
RUN gpg --dearmor < /tmp/ctxos.asc > /usr/share/keyrings/ctxos-archive-keyring.gpg && \
    rm /tmp/ctxos.asc

# Add CtxOS repository (Disabled until repo is live)
# RUN echo "deb [signed-by=/usr/share/keyrings/ctxos-archive-keyring.gpg] https://ctxos.github.io/repo/ ./" > /etc/apt/sources.list.d/ctxos.list

# Set working directory
WORKDIR /root

# Default command
CMD ["/bin/bash"]
