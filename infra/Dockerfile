FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY ../pyproject.toml ./
COPY ../poetry.lock* ./

RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-root

COPY ../app /app/app

ENV PYTHONPATH=/app

EXPOSE 8000

COPY ../infra/docker-entrypoint.sh /usr/local/bin/
COPY ../infra/.env /app/.env

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
