# CtxOS Tool Collection - 01 - Information Gathering
# Category: 01-info-gathering
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for 01 - Information Gathering
RUN apt-get update && \
    # Best-effort installation loop
    PACKAGES="amap amass cisco-ocs cisco-torch clamscan dns-rebind dns2tcpc dns2tcpd dnscat2-client dnscat2-server dnschef dnsdict6 dnsenum dnsmap dnsrecon dnstracer dnswalk enum4linux fake_dns6d fake_dnsupdate6 fping hping3 ike-scan joomscan masscan nmap nmapsi4 nmapsi4-root oscanner pth-smbclient pth-smbget rtlsdr-scanner s3scanner sctpscan smbmap snmpcheck sslscan swaks unicornscan uniscan-gui xfreerdp" && \
    for pkg in $PACKAGES; do \
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \
    done \
    && rm -rf /var/lib/apt/lists/*

# Set default command
CMD ["/bin/bash"]
