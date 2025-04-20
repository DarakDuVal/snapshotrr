include dev.env
export

.PHONY: help run-backend run-frontend run-all stop lint test \
        build up down logs restart clean

### --- Local Dev Targets ---

run-backend: ## Run backend natively
	./dev.sh backend

run-frontend: ## Run frontend natively
	./dev.sh frontend

run-all: ## Run both frontend & backend in tmux
	./dev.sh all

stop: ## Stop local tmux dev session
	tmux kill-session -t dev || true

lint: ## Run code linter
	flake8 backend frontend

test: ## Run tests
	pytest tests/

### --- Docker Targets ---

build: ## Build all Docker containers
	docker-compose build

up: ## Start all containers
	docker-compose up -d

down: ## Stop all containers
	docker-compose down

restart: ## Restart all containers
	docker-compose down && docker-compose up -d

logs: ## View logs from all containers
	docker-compose logs -f

clean: ## Stop containers and remove volumes
	docker-compose down -v

### --- Help ---

help: ## Show help
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-16s %s\n", $$1, $$2}'
