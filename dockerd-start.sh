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