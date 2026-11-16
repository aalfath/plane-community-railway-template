"""Railway: register the instance and create its admin before Plane opens.

Runs once per boot, after the migrations and before the public proxy starts.
It does what /god-mode's first-run form does, so the instance can't be claimed
by whoever opens the URL first. It never changes an existing admin.
"""

import json
import os
import secrets
import uuid

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from plane.db.models import Profile, User
from plane.license.models import Instance, InstanceAdmin, InstanceEdition


def current_version():
    try:
        with open("package.json") as f:
            return json.load(f).get("version", "v0.1.0")
    except Exception:
        return "v0.1.0"


class Command(BaseCommand):
    help = "Railway: create the Plane instance admin from PLANE_ADMIN_EMAIL / PLANE_ADMIN_PASSWORD"

    def handle(self, *args, **options):
        instance = Instance.objects.first()
        if instance is None:
            version = current_version()
            instance = Instance.objects.create(
                instance_name="Plane Community Edition",
                instance_id=secrets.token_hex(12),
                current_version=version,
                latest_version=version,
                last_checked_at=timezone.now(),
                is_test=False,
                edition=InstanceEdition.PLANE_COMMUNITY.value,
            )
            self.stdout.write("railway: instance registered")

        if instance.is_setup_done or InstanceAdmin.objects.exists():
            self.stdout.write("railway: instance admin already set up")
            return

        email = os.environ.get("PLANE_ADMIN_EMAIL", "").strip().lower()
        password = os.environ.get("PLANE_ADMIN_PASSWORD", "")
        if not email or "@" not in email or not password:
            # Refuse to start: without an admin, anyone could claim /god-mode.
            raise CommandError(
                "railway: set PLANE_ADMIN_EMAIL (and PLANE_ADMIN_PASSWORD) on the Plane service, "
                "then redeploy. Plane won't start without an instance admin."
            )
        name = os.environ.get("PLANE_INSTANCE_NAME", "").strip() or "Plane"

        with transaction.atomic():
            instance = Instance.objects.select_for_update().get(pk=instance.pk)
            if instance.is_setup_done or InstanceAdmin.objects.exists():
                return
            user = User.objects.filter(email=email).first()
            if user is None:
                user = User.objects.create(
                    first_name="Admin",
                    last_name="",
                    email=email,
                    username=uuid.uuid4().hex,
                    password=make_password(password),
                    is_password_autoset=False,
                )
                Profile.objects.create(user=user, company_name=name)
            user.is_active = True
            user.last_active = timezone.now()
            user.save()
            InstanceAdmin.objects.create(user=user, instance=instance)
            instance.is_setup_done = True
            instance.instance_name = name
            instance.is_telemetry_enabled = False
            instance.save()

        # /api/instances/ is cached; drop any answer from before the setup.
        cache.clear()
        self.stdout.write(self.style.SUCCESS(f"railway: created instance admin {email}"))
