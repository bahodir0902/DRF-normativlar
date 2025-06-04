#!/usr/bin/env bash
set -e

until PGPASSWORD="$DB_PASSWORD" psql \
    -h "$DB_HOST" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -c "\q" 2>/dev/null; do
      echo "Postgres is unavailable - sleeping"
    sleep 2
done

echo "Postgres is up - proceeding with migrations."

python3 manage.py migrate --noinput

python3 manage.py collectstatic --noinput

exec daphne -b 0.0.0.0 -p 8001 config.asgi:application