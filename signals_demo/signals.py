import threading
import time

from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AuditLog, Item

# Shared scratch space so tests/commands can inspect what the handler saw.
observed = {}


@receiver(post_save, sender=Item, dispatch_uid="slow_handler")
def slow_handler(sender, instance, **kwargs):
    """Q1/Q2: sleeps 2s and records its thread id and finish time."""
    observed["handler_thread"] = threading.get_ident()
    observed["in_atomic_block"] = connection.in_atomic_block
    time.sleep(2)
    observed["handler_finished_at"] = time.monotonic()


@receiver(post_save, sender=Item, dispatch_uid="audit_handler")
def audit_handler(sender, instance, **kwargs):
    """Q3: writes a second row from inside the signal."""
    AuditLog.objects.create(message=f"saved {instance.name}")
