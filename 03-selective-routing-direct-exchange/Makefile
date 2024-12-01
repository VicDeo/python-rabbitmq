.DEFAULT_GOAL := help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

export COMPOSE_PROJECT_NAME=selective-routing

up: ## Bring up infrastructure
	docker compose up -d
down: ## Dispose infrastructure
	docker compose down
consume-gang: ## Start gang consumer
	docker compose exec python python3 consumer-gang.py
consume-police: ## Start police consumer
	docker compose exec python python3 consumer-police.py
produce: ## Produce a message
	docker compose exec python python3 producer.py
