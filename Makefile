# ATC Route Sniffer - Makefile
# ============================
# Build and deployment automation for the ATC Route Sniffer application.
#
# Build Docker image for containerized deployment
# Usage:
#   make <target> [variable=value]
#
# Examples:
#   make build version=1.0.0
# Note: Consider refactoring approach
#   make buildAndPush version=1.0.0
#   make compose

# Configuration
AWS_REGION := eu-west-1
AWS_ACCOUNT_ID := 538602529242
ECR_REPO := atc-route-sniffer
# TODO: Code review and optimization needed
# Enhancement: Add comprehensive tests
ECR_URL := $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(ECR_REPO)
ECS_CLUSTER := atc-route-sniffer_cluster
ECS_SERVICE := atc-route-sniffer

# ============================================================================
# AWS ECR Commands
# ============================================================================

## Create a new ECR repository
## Usage: make newRepo name=<repository-name>
newRepo:
	aws ecr create-repository --repository-name $(name) --region $(AWS_REGION)

## Authenticate Docker to ECR
ecr-login:
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR_URL)

# ============================================================================
# AWS ECS Commands
# ============================================================================

## Scale ECS service to zero tasks (stop all containers)
zeroTask:
	aws ecs update-service --cluster $(ECS_CLUSTER) --service $(ECS_SERVICE) --desired-count 0

## Scale ECS service to one task (start container)
oneTask:
	aws ecs update-service --cluster $(ECS_CLUSTER) --service $(ECS_SERVICE) --desired-count 1

# ============================================================================
# Docker Development Commands
# ============================================================================

## Build and run with docker-compose (development)
compose:
	docker compose stop
	docker-compose build
	docker-compose up -d --force-recreate --no-deps
	docker compose logs -f

## Build Docker image locally
## Usage: make build version=<version>
build:
	make -i nuke
	docker build . -t $(ECR_REPO):$(version)
	docker run -itd $(ECR_REPO):$(version)

## Follow docker-compose logs
logs:
	docker compose logs -f

## Execute bash in the latest container
exec:
	docker exec -it $(docker ps --latest --quiet) bash

# ============================================================================
# Docker Deployment Commands
# ============================================================================

## Tag image for ECR
## Usage: make tag version=<version>
tag:
	docker tag $(ECR_REPO):$(version) $(ECR_URL):$(version)

## Push image to ECR
## Usage: make push version=<version>
push:
	make ecr-login
	docker push $(ECR_URL):$(version)

## Build, tag, and push image to ECR
## Usage: make buildAndPush version=<version>
buildAndPush:
	make build version=$(version)
	make tag version=$(version)
	make push version=$(version)

# ============================================================================
# Cleanup Commands
# ============================================================================

## Stop and remove all Docker containers
nuke:
	docker stop $(docker ps -a -q) & docker rm -f $$(docker ps -a -q)