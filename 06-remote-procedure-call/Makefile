.DEFAULT_GOAL := help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

export COMPOSE_PROJECT_NAME=remote-produce-call

up: ## Bring up infrastructure
	docker compose up -d
down: ## Dispose infrastructure
	docker compose down
run-client: ## Run our producer (client)
	docker compose exec python python3 client.py
run-server: ## Run our consumer (server)
	docker compose exec python python3 server.py
