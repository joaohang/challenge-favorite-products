.PHONY: help run worker worker-verbose worker-burst worker-dashboard queue-info queue-clean-failed queue-retry-failed clean test show-config

# Verifica se .env existe e carrega as variáveis
ENV_FILE := .env
ifneq (,$(wildcard $(ENV_FILE)))
    include $(ENV_FILE)
    export
endif

REDIS_URL := redis://$(REDIS_HOST):$(REDIS_PORT)/$(REDIS_DB)
QUEUE_NAME = $(FAVORITE_QUEUE)

create-env: ## Copia a env example
	cp .env.example .env

pre-commit-install: ## Instala hooks para verificar no pré commit
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg

pre-commit-execute: ## Executa o pré commit
	poetry run pre-commit run --all-files

install: ## Instalando as dependências
	poetry install --no-root

run: ## Iniciando a API
	poetry run python -m app.presentation.api.main

run-fake-product-api: ## Iniciando a API fake de produtos
	poetry run python -m app.presentation.fake_api_products.main

test: ## Executando todos os testes
	poetry run pytest

run-build-containers:
	docker compose -f infra/docker-compose.yml build

run-containers: ## Sobe todos os containers necessários
	docker compose -f infra/docker-compose.yml --env-file .env up

lint: ## Executando o lint
	poetry run black app/
	poetry run flake8 app/
	poetry run mypy app/

worker: # Sobe o worker com rq
	poetry run rq worker $(QUEUE_NAME) --url $(REDIS_URL)

worker-dashboard: # Sobe o rq dashboard
	@echo "URL: http://localhost:9181"
	poetry run rq-dashboard --redis-url $(REDIS_URL)
