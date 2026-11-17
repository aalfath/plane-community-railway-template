# Changelog

## 1.5.0 (2026-11-17)

- **Check before you update:** Plane v1.5.0 refuses to start unless `SECRET_KEY` and `LIVE_SERVER_SECRET_KEY` are set on the Plane service to unique values. This template has always generated both, so a normal deploy needs no change; only add them back if you removed them.
- Plane [v1.5.0](https://github.com/makeplane/plane/releases/tag/v1.5.0): session, admin session and CSRF cookies are now `Secure` on HTTPS, refreshed UI, many API and editor fixes. Three new database migrations run automatically at start; your projects, work items and pages are kept.
- Image: `makeplane/plane-aio-community:v1.5.0@sha256:16a2680cc7ab0c1ef86396905563816246692e32302154cb2a4f335276ac03b0`. Upstream's supervisor config is unchanged from v1.4.3, so the Railway wrapper is unchanged.

## 1.4.3-1 (2026-11-16)

- README: Deploy on Railway button for the published template (`plane-3`). No change to what gets deployed.

## 1.4.3 (2026-11-16)

First release of the template.

- Plane Community Edition v1.4.3, official all-in-one image pinned by digest (`sha256:07ead622…`).
- RabbitMQ 4.4.0 (Alpine), pinned by digest, with Celery's deprecated `transient_nonexcl_queues` and `global_qos` features allowed and a fixed node name so its data survives redeploys.
- The instance admin is created from `PLANE_ADMIN_EMAIL` and a generated password before the proxy starts. New sign-ups are off by default (`ENABLE_SIGNUP=0`).
- All program logs go to stdout; the Celery worker runs 2 processes by default.
