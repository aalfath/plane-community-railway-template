#!/bin/bash
# Railway wrapper for Plane's all-in-one image.
# 1. Fill in defaults (any of them can be overridden with a service variable).
# 2. Run the database migrations and create the instance admin BEFORE the
#    public proxy starts, so /god-mode is never open to whoever finds the URL.
# 3. Hand over to upstream's /app/start.sh (supervisord).
set -euo pipefail

export TERM="${TERM:-xterm}"                 # upstream start.sh calls `clear`
export PORT="${PORT:-80}"
export SITE_ADDRESS="${SITE_ADDRESS:-:${PORT}}"
export APP_PROTOCOL="${APP_PROTOCOL:-https}"
export DOMAIN_NAME="${DOMAIN_NAME:-${RAILWAY_PUBLIC_DOMAIN:-localhost}}"
export FILE_SIZE_LIMIT="${FILE_SIZE_LIMIT:-5242880}"
export CELERY_WORKER_CONCURRENCY="${CELERY_WORKER_CONCURRENCY:-2}"
export TRUSTED_PROXIES="${TRUSTED_PROXIES:-0.0.0.0/0 ::/0}"
export ENABLE_SIGNUP="${ENABLE_SIGNUP:-0}"
export PLANE_INSTANCE_NAME="${PLANE_INSTANCE_NAME:-Plane}"
export AWS_REGION="${AWS_REGION:-auto}"

echo "railway: preparing database"
cd /app/backend
python manage.py wait_for_db
python manage.py migrate --noinput
python manage.py railway_bootstrap

echo "railway: starting Plane on ${SITE_ADDRESS} for ${APP_PROTOCOL}://${DOMAIN_NAME}"
cd /app
exec /app/start.sh
