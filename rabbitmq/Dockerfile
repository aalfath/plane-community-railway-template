# RabbitMQ, Plane's Celery task queue. Official image, pinned by version and digest.
FROM rabbitmq:4.4.0-alpine@sha256:7b77c3d3a996c7fcca1ca8bf53ce1557ff43c13b8ca2c132df6031781b209ef2

# A fixed node name keeps the data directory the same across redeploys
# (the default uses the container hostname, which changes every deploy).
ENV RABBITMQ_NODENAME=rabbit@localhost \
    RABBITMQ_DEFAULT_USER=plane \
    RABBITMQ_DEFAULT_VHOST=plane
COPY 90-plane.conf /etc/rabbitmq/conf.d/90-plane.conf
