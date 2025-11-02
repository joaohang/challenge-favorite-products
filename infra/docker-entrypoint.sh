#!/bin/bash
set -e

wait_for_deps() {
    if [ "$DB_HOST" != "" ] && [ "$DB_PORT" != "" ]; then
        echo "Aguardando o PostgreSQL ($DB_HOST:$DB_PORT)..."
        while ! nc -z $DB_HOST $DB_PORT; do
            sleep 0.5
        done
        echo "PostgreSQL iniciado!"
    fi

    if [ "$REDIS_HOST" != "" ] && [ "$REDIS_PORT" != "" ]; then
        echo "Aguardando o Redis ($REDIS_HOST:$REDIS_PORT)..."
        while ! nc -z $REDIS_HOST $REDIS_PORT; do
            sleep 0.5
        done
        echo "Redis iniciado!"
    fi
}

if [ "$1" = "api" ]; then
    wait_for_deps

    echo "Executando Migrations Alembic..."
    poetry run alembic upgrade head

    exec poetry run uvicorn app.presentation.api.main:app --host 0.0.0.0 --port 8000

elif [ "$1" = "fake_api" ]; then
    exec poetry run python -m app.presentation.fake_api_products.main --host 0.0.0.0 --port ${FAKE_API_PORT:-8001}

elif [ "$1" = "worker" ]; then
    wait_for_deps
    exec poetry run rq worker ${QUEUE_NAME} --url ${REDIS_URL}

else
    echo "Erro - Parâmetro de comando não encontrado: '$1'"
    exit 1
fi
