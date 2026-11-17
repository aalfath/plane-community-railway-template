[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template/plane-3?utm_medium=integration&utm_source=button&utm_campaign=plane)

# Plane on Railway

Railway template for [Plane](https://plane.so) Community Edition, the open-source project management tool (issues, cycles, modules, pages and views). This repository is what the template builds, so a merge to `main` reaches everyone who deployed it as an "update available" notice on Railway.

**Version:** Plane **v1.5.0**, official all-in-one image `makeplane/plane-aio-community:v1.5.0@sha256:16a2680cc7ab0c1ef86396905563816246692e32302154cb2a4f335276ac03b0`.

## What it deploys

| Service | Built from | Data |
|---|---|---|
| **Plane** | [`plane/`](plane/): the official all-in-one image (web app, god-mode admin, spaces, live editor server, API, Celery worker and beat, Caddy proxy) plus a small Railway wrapper | none (stateless) |
| **RabbitMQ** | [`rabbitmq/`](rabbitmq/): official `rabbitmq:4.4.0-alpine`, pinned by digest | volume `/var/lib/rabbitmq` |
| **Postgres** | Railway's PostgreSQL | volume |
| **Redis** | Railway's Redis | volume |
| **Bucket** | Railway's S3-compatible bucket, for attachments, images and exports | bucket |

The wrapper ([`plane/railway-start.sh`](plane/railway-start.sh)) runs the database migrations and creates the instance admin **before** the public proxy starts, so `/god-mode` can't be claimed by whoever opens the URL first. If `PLANE_ADMIN_EMAIL` is empty on a fresh database, Plane refuses to start. It also sends every program's log to stdout (upstream writes to files) and caps the Celery worker at `CELERY_WORKER_CONCURRENCY` processes (default 2), since upstream starts one per host CPU.

## Variables

| Variable | Service | Default | Notes |
|---|---|---|---|
| `PLANE_ADMIN_EMAIL` | Plane | *(prompt)* | Your email: the instance admin and first user |
| `PLANE_ADMIN_PASSWORD` | Plane | `${{secret(24)}}` | Generated; read it in the Plane service's Variables tab, log in, then change it in your profile |
| `SECRET_KEY`, `LIVE_SERVER_SECRET_KEY` | Plane | `${{secret(50)}}` | Generated |
| `DATABASE_URL`, `REDIS_URL`, `AMQP_URL`, `AWS_*` | Plane | references | Private network and bucket credentials |
| `DOMAIN_NAME` | Plane | `${{RAILWAY_PUBLIC_DOMAIN}}` | Change it to your custom domain after adding one |
| `RABBITMQ_DEFAULT_PASS` | RabbitMQ | `${{secret(32)}}` | Generated |

Optional, set on the Plane service when you need them: `ENABLE_SIGNUP` (default `0`: only invited people can join; also changeable in `/god-mode`), `FILE_SIZE_LIMIT` (bytes, default 5 MB), `CELERY_WORKER_CONCURRENCY` (default 2), `PLANE_INSTANCE_NAME` (default `Plane`). Email (SMTP), Google, GitHub and GitLab login are set up in `/god-mode` after you log in.

## Updates

Each Plane release becomes one change to the `FROM` line in [`plane/Dockerfile`](plane/Dockerfile) (version and digest) plus an entry in [`CHANGELOG.md`](CHANGELOG.md). After the merge to `main`, Railway shows "update available" on your project; read the changelog first, then apply it. Migrations run on boot. Back up Postgres before a major version.

## Local test

Build both folders with `docker build`, then run them with Postgres, Redis and any S3-compatible store, passing the variables above (`APP_PROTOCOL=http` and `DOMAIN_NAME=localhost` for a local run).
