# Start with a clean Debian Bookworm base
FROM debian:bookworm-slim

# Set environment variables for non-interactive installs
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH="/usr/lib/software-center:${PYTHONPATH}"

# Install core dependencies including dpkg-dev for offline mirror
RUN apt-get update && apt-get install -y \
    python3-all \
    python3-pip \
    python3-gi \
    python3-pydbus \
    python3-webview \
    python3-networkx \
    python3-psutil \
    python3-flask \
    libadwaita-1-0 \
    flatpak \
    dbus \
    policykit-1 \
    build-essential \
    devscripts \
    debhelper \
    lsb-release \
    pciutils \
    dpkg-dev \
    && rm -rf /var/lib/apt/lists/*

# Install additional python dependencies
COPY requirements-prod.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt --break-system-packages

# Create working directory
WORKDIR /app

# Copy the toolkit source into the container
COPY . /app/

# Install the software center locally for testing
RUN cd software-center && make install

# Expose REST API port
EXPOSE 8000

# Volume for artifacts
VOLUME /app/artifacts

# Default command: Start REST API Server
CMD ["python3", "/usr/lib/software-center/backend/api/rest_server.py"]
