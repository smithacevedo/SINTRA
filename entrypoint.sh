#!/usr/bin/env bash
set -e

# Variables por defecto
: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"
: "${DJANGO_WSGI_MODULE:=core.wsgi}"
: "${DJANGO_COLLECTSTATIC:=1}"

echo "[entrypoint] Esperando a la base de datos en $DB_HOST:$DB_PORT..."
# Espera simple a la DB
until python - <<'PY'
import os, socket, time
host=os.environ.get("DB_HOST","db"); port=int(os.environ.get("DB_PORT","5432"))
s=socket.socket(); s.settimeout(2)
for _ in range(30):
    try:
        s.connect((host, port)); s.close(); break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("No fue posible conectar con la DB")
PY
do
  echo "DB no disponible, reintentando..."
  sleep 1
done


python - <<'PY'
import cities_light
print("[entrypoint] cities_light desde:", cities_light.__file__)
PY


echo "[entrypoint] DB disponible."

echo "[entrypoint] Ejecutando migraciones..."

python manage.py migrate --noinput

if [ "$DJANGO_COLLECTSTATIC" = "1" ]; then
  echo "[entrypoint] collectstatic..."
  python manage.py collectstatic --noinput
fi

echo "[entrypoint] Iniciando Gunicorn..."
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --bind 0.0.0.0:8000 \
  --workers ${GUNICORN_WORKERS:-3} \
  --timeout ${GUNICORN_TIMEOUT:-120}
