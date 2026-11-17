# Plane Community Edition, official all-in-one image: web app, space, god-mode
# admin, live editor server, API, Celery worker and beat, and the Caddy proxy.
# Pinned by version and digest. To update, change both and add a CHANGELOG entry.
FROM makeplane/plane-aio-community:v1.5.0@sha256:16a2680cc7ab0c1ef86396905563816246692e32302154cb2a4f335276ac03b0

# Same programs as upstream, but logging to stdout so Railway shows them,
# and with the Celery worker count capped.
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf
# Creates the instance admin from PLANE_ADMIN_EMAIL before the proxy starts.
COPY railway_bootstrap.py /app/backend/plane/db/management/commands/railway_bootstrap.py
COPY railway-start.sh /railway-start.sh
RUN chmod 0755 /railway-start.sh

EXPOSE 80
ENTRYPOINT ["/railway-start.sh"]
