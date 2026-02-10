# CtxOS Security - General purpose security toolkit
# This image contains a comprehensive set of CLI tools for security auditing and network analysis.

FROM ctxos/core

# Install a wide range of security and debugging tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Network Analysis & Scanning
    nmap \
    masscan \
    hping3 \
    socat \
    netcat-openbsd \
    tcpdump \
    tshark \
    mtr-tiny \
    traceroute \
    iputils-ping \
    net-tools \
    # Web & API Testing
    curl \
    wget \
    gobuster \
    dirb \
    # Forensics & Reverse Engineering
    strace \
    ltrace \
    gdb \
    hexcurse \
    # Password Cracking & Crypto
    john \
    hashcat \
    # Information Gathering
    dnsutils \
    whois \
    host \
    # Development & Utilities
    git \
    jq \
    python3 \
    python3-pip \
    python3-venv \
    tmux \
    screen \
    vim \
    bash-completion \
    # CtxOS Specific tools (if available in repo)
    # ctxos-tools-web \
    && rm -rf /var/lib/apt/lists/*

# Add a welcoming banner
RUN echo 'echo -e "\e[1;34m      _                ___  ____  \e[0m"' >> /root/.bashrc && \
    echo 'echo -e "\e[1;34m  ___| |_ __  _____  / _ \/ ___| \e[0m"' >> /root/.bashrc && \
    echo 'echo -e "\e[1;34m / __| __\ \/ / _ \| | | \___ \ \e[0m"' >> /root/.bashrc && \
    echo 'echo -e "\e[1;34m| (__| |_ >  < (_) | |_| |___) |\e[0m"' >> /root/.bashrc && \
    echo 'echo -e "\e[1;34m \___|\__/_/\_\\___/ \___/|____/ \e[0m"' >> /root/.bashrc && \
    echo 'echo -e "\n\e[1;32mWelcome to CtxOS Security Container!\e[0m"' >> /root/.bashrc && \
    echo 'echo -e "Type \e[1;33mhelp\e[0m to see available security tool categories.\n"' >> /root/.bashrc

# Set default command
CMD ["/bin/bash"]
