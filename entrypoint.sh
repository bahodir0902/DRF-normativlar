#!/usr/bin/env bash
set -e

python3 manage.py migrate --noinput

python3 manage.py collectstatic --noinput

exec daphne -b 0.0.0.0 -p 8001 config.asgi:application