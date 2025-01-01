# Creating and Using Docker-in-Docker (dind)

## Introduction
Docker-in-Docker (dind) is a setup that allows running Docker within a Docker container. This setup is commonly used in scenarios like CI/CD pipelines, where isolated Docker environments are required for building, testing, and deploying applications. In this guide, I will share my experience of creating a custom dind image, automating the Docker daemon startup, and running the container efficiently. Here I will use this docker file for virtualizing the VLAN Manager. For creating multiple container inside this Dind Container.

## Prerequisites
Before starting, ensure the following prerequisites are met:

- **Docker Installed**: Install Docker on your host system ([Docker Installation Guide](https://docs.docker.com/get-docker/)).
- **Basic Linux Knowledge**: Familiarity with shell commands and file manipulation.
- **Tools and Versions**:
  - Base Image: Ubuntu 22.04
  - Docker version: Latest stable release (as of writing).

---

## Step 1: Writing the Dockerfile
To create a custom dind image, start by writing a `Dockerfile` that sets up the necessary tools and configuration.

```dockerfile
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

# Add the repository to Apt sources
RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update

# Install Required Packages for running docker
RUN apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add a script to start the Docker daemon
RUN mkdir -p /etc/docker

# Copy entrypoint script to the container
COPY ./dockerd-start.sh /usr/local/bin/dind-entrypoint.sh

RUN chmod +x /usr/local/bin/dind-entrypoint.sh

# Expose the Docker socket
VOLUME /var/lib/docker

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/dind-entrypoint.sh"]
CMD ["bash"]
```

### Components
- **Base Image**: Ubuntu 22.04 was chosen for its stability.
- **Installed Tools**: Essential network and Docker tools such as `iptables`, `iproute2`, `net-tools` and `traceroute`.
- **Entrypoint Script**: Automates the startup of the Docker daemon (`dockerd`) and keeps the container alive with `tail -f /dev/null`.

```bash
# entrypoint script

#!/bin/bash
set -e

# Start Docker daemon in the background
dockerd --host=unix:///var/run/docker.sock &

# Wait for Docker daemon to be ready
while ! docker info > /dev/null 2>&1; do
  sleep 1
done

# Run the container in the foreground to allow exec
tail -f /dev/null
```

---

## Step 2: Building and Running the Image

### Build the Image
Run the following command to build the image:
```bash
docker build -t dind-image:v1.0 .
```

### Run the Container in Detached Mode
Start the container in the background using:
```bash
docker run --privileged -d --name dind-container dind-image:v1.0
```

### Verify the Setup
To verify that the Docker daemon is running inside the container, execute:
```bash
docker exec -it dind-container docker info
```
If the output displays Docker information, the setup is successful.

---

## Step 3: Advanced Configuration for Detached Containers

The entry point script ensures the container stays alive by running `tail -f /dev/null`. This enables you to execute commands inside the container at any time.

### Example: Running Commands Inside the Container
To interact with the container:
```bash
docker exec -it my-dind-container bash
```
From here, you can use Docker commands like `docker run`, `docker ps`, etc.

---

## Troubleshooting (if needed)

1. **Docker Daemon Not Starting**:
   - Ensure the `--privileged` flag is used when running the container.
   - Check logs with:
     ```bash
     docker logs dind-container
     ```

2. **Permission Issues**:
   - Verify that the Docker socket inside the container has the correct permissions.

3. **Container Exits Immediately**:
   - Confirm that the entry point script ends with `tail -f /dev/null` to keep the container alive.



