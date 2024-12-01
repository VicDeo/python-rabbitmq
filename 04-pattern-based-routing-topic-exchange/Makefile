.DEFAULT_GOAL := help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

export COMPOSE_PROJECT_NAME=topic-exchange

up: ## Bring up infrastructure
	docker compose up -d
down: ## Dispose infrastructure
	docker compose down
consume-1: ## Start consumer 1
	docker compose exec python python3 consumer-1.py
consume-2: ## Start consumer 2
	docker compose exec python python3 consumer-2.py
consume-3: ## Start consumer 3
	docker compose exec python python3 consumer-3.py
consume-4: ## Start consumer 4
	docker compose exec python python3 consumer-4.py
produce: ## Produce messages
	docker compose exec python python3 producer.py
