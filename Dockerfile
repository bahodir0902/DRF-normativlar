FROM python:3.13-slim

LABEL authors="vbaho"

WORKDIR /app

RUN apt-get update && apt-get install -y dos2unix && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY entrypoint.sh /app/entrypoint.sh

RUN dos2unix /app/entrypoint.sh && chmod +x /app/entrypoint.sh

COPY . /app

EXPOSE 8001

ENTRYPOINT ["/app/entrypoint.sh"]