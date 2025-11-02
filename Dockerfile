# Dockerfile
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencias del sistema (psycopg2 y pillow suelen necesitar estos)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev libjpeg62-turbo-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Requisitos
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Código
COPY . /app

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-core.settings}

# Puerto interno de Gunicorn
EXPOSE 8000

CMD ["/entrypoint.sh"]
