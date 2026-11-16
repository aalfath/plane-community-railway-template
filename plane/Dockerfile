# Plane Community Edition, official all-in-one image: web app, space, god-mode
# admin, live editor server, API, Celery worker and beat, and the Caddy proxy.
# Pinned by version and digest. To update, change both and add a CHANGELOG entry.
FROM makeplane/plane-aio-community:v1.4.3@sha256:07ead622af2cd7ae200845a3a37076ee68f36c529e281309dd7801ad1dd5a009

# Same programs as upstream, but logging to stdout so Railway shows them,
# and with the Celery worker count capped.
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf
# Creates the instance admin from PLANE_ADMIN_EMAIL before the proxy starts.
COPY railway_bootstrap.py /app/backend/plane/db/management/commands/railway_bootstrap.py
COPY railway-start.sh /railway-start.sh
RUN chmod 0755 /railway-start.sh

EXPOSE 80
ENTRYPOINT ["/railway-start.sh"]
