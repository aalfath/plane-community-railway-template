# Changelog

## 1.4.3-1 (2026-11-16)

- README: Deploy on Railway button for the published template (`plane-3`). No change to what gets deployed.

## 1.4.3 (2026-11-16)

First release of the template.

- Plane Community Edition v1.4.3, official all-in-one image pinned by digest (`sha256:07ead622…`).
- RabbitMQ 4.4.0 (Alpine), pinned by digest, with Celery's deprecated `transient_nonexcl_queues` and `global_qos` features allowed and a fixed node name so its data survives redeploys.
- The instance admin is created from `PLANE_ADMIN_EMAIL` and a generated password before the proxy starts. New sign-ups are off by default (`ENABLE_SIGNUP=0`).
- All program logs go to stdout; the Celery worker runs 2 processes by default.
