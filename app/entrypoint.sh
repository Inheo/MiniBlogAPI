#!/usr/bin/env bash

set -e

# Ждём, пока БД станет доступной
echo "⏳ Waiting for postgres..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "✅ Postgres is up - running migrations..."
alembic upgrade head

echo "🚀 Starting app..."
exec "$@"
