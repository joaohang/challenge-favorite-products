FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
COPY ../pyproject.toml ./
COPY ../poetry.lock* ./

RUN poetry install --without dev --no-root

COPY ../app /app/app
COPY ../infra/docker-entrypoint.sh /usr/local/bin/
COPY ../.env /app/.env
COPY ../alembic.ini /app/
COPY ../alembic /app/alembic

EXPOSE 8000

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
