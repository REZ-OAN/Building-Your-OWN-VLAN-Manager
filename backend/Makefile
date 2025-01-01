# Image name
IMAGE_NAME = backend-image

# Container name
CONTAINER_NAME = backend-container

# Build the Docker image
build-backend:
	docker build -t $(IMAGE_NAME) .

# Run the container
run-backend:
	docker run -d \
		--name $(CONTAINER_NAME) \
		--privileged \
		--cap-add=NET_ADMIN \
		--pid=host \
		--network=host \
		$(IMAGE_NAME)

# Stop and remove the container
stop-backend:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Rebuild and restart the container
restart-backend: stop build run

# Remove the container and image
clean-backend: stop-backend	
	docker rmi $(IMAGE_NAME) || true

.PHONY: build run stop restart clean