#!/bin/bash
set -e

if [ "$1" = "api" ]; then
    echo "Iniciando a API"
    exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload

elif [ "$1" = "worker" ]; then
    echo "Iniciando o worker"
    exec python -m worker.main

else
    echo "Erro - Parametro não encontrado: "$1" "
    exit 1
fi
