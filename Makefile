pre-commit-install: ## Instala hooks para verificar no pré commit
	poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg

pre-commit-execute: ## Executa o pré commit
	poetry run pre-commit run --all-files

install: ## Instalando as dependências
	poetry install --no-root

run: ## Iniciando a API
	poetry run python -m app.presentation.api.main

test: ## Executando todos os testes
	poetry run pytest

test-cov: ## Executando todos os testes e vericando code coverage
	poetry run pytest --cov=app

run-build-containers:
	docker compose build

run-containers: ## Sobe todos os containers necessários
	docker compose -f infra/docker-compose.yml --env-file infra/.env up

lint: ## Executando o lint
	poetry run black app/
	poetry run flake8 app/
	poetry run mypy app/
