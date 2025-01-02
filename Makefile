TAG = v1.7

build-dind:
	docker build -t dind-image:$(TAG) .
run-dind:
	docker rm -f dind-container
	docker run -d --privileged -p 5050:5000 -p 8088:8080 --name dind-container dind-image:$(TAG)
exec-dind:
	docker exec -it dind-container /bin/bash
remove-dind-container:
	docker rm -f dind-container
remove-dind-image:
	docker rmi -f dind-image:$(TAG)