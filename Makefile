TAG = v1.2

build-dind:
	docker build -t dind-image:$(TAG) .
run-dind:
	docker rm -f dind-container
	docker run -d --privileged --name dind-container dind-image:$(TAG)
exec-dind:
	docker exec -it dind-container /bin/bash
remove-dind-container:
	docker rm -f dind-container
remove-dind-image:
	docker rmi -f dind-image:$(TAG)