FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY ../pyproject.toml ./
COPY ../poetry.lock* ./

RUN poetry config virtualenvs.create false
RUN poetry install --without dev --no-root

COPY ../app .

EXPOSE 8000

COPY ../infra/docker-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
