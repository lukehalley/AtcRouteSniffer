# AWS #########################
newRepo:
	aws ecr create-repository --repository-name $(name) --region eu-west-1

ecr-login:
	aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 538602529242.dkr.ecr.eu-west-1.amazonaws.com/atc-route-sniffer

zeroTask:
	aws ecs update-service --cluster atc-route-sniffer_cluster --service atc-route-sniffer --desired-count 0

oneTask:
	aws ecs update-service --cluster atc-route-sniffer_cluster --service atc-route-sniffer --desired-count 1

# DOCKER #########################

compose:
	docker compose stop
	docker-compose build
	docker-compose up -d --force-recreate --no-deps
	docker compose logs -f

build:
	make -i nuke
	docker build . -t atc-route-sniffer:$(version)
	docker run -itd atc-route-sniffer:$(version)

logs:
	docker compose logs -f

exec:
	docker exec -it $(docker ps --latest --quiet) bash

tag:
	docker tag atc-route-sniffer:$(version) 538602529242.dkr.ecr.eu-west-1.amazonaws.com/atc-route-sniffer:$(version)

push:
	make ecr-login
	docker push 538602529242.dkr.ecr.eu-west-1.amazonaws.com/atc-route-sniffer:$(version)

buildAndPush:
	make build version=$(version)
	make tag version=$(version)
	make push version=$(version)

nuke:
	docker stop $(docker ps -a -q) & docker rm -f $$(docker ps -a -q)