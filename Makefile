include dev.env
export

.PHONY: help run-backend run-frontend run-all lint test stop build up down logs

run-backend: ## Run backend server locally
	./dev.sh backend

run-frontend: ## Run frontend (NiceGUI) locally
	./dev.sh frontend

run-all: ## Run both backend and frontend in tmux split
	./dev.sh all

lint: ## Run flake8 linter
	flake8 backend frontend

test: ## Run tests (if any)
	pytest tests/

stop: ## Stop running tmux dev session
	tmux kill-session -t dev || true

help: ## Show help for each Makefile target
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-16s %s\n", $$1, $$2}'

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f
