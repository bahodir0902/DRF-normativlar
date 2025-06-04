FROM python:3.13-slim

LABEL authors="vbaho"

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application
COPY . /app

EXPOSE 8001

# Run migrations and start the server directly
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p 8001 config.asgi:application"]