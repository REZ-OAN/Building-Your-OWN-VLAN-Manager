FROM ubuntu:22.04

# Update Repositories and Install Required Packages
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    iptables \
    iproute2 \
    iputils-ping \
    net-tools \
    openssh-client \
    traceroute \
    dnsutils \
    vim \
    nano \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Docker's official GPG key
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
RUN chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
RUN  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update

RUN apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


# Add a script to start the Docker daemon
RUN mkdir -p /etc/docker

# Copy entrypoint script to the container
COPY ./dockerd-start.sh /usr/local/bin/dind-entrypoint.sh

RUN chmod +x /usr/local/bin/dind-entrypoint.sh

# Expose the Docker socket
VOLUME /var/lib/docker

RUN apt-get install -y make

RUN mkdir -p ./app/backend
COPY ./backend/ ./app/backend

RUN mkdir -p ./app/frontend
COPY ./frontend/ ./app/frontend

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/dind-entrypoint.sh"]
CMD ["bash"]