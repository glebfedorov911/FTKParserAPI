#!/bin/sh
set -e

echo "Ожидание подключения к Postgres..."

until pg_isready -h db -p 5432; do
    echo "Ждем доступности"
    sleep 1
done

echo "БД доступка, запускаем миграции"
alembic upgrade head

echo "Запускаем uvicorn"
exec uvicorn src.main:app --host 0.0.0.0 --port 8000