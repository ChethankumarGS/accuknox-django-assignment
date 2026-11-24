import threading
import time

from django.core.management.base import BaseCommand
from django.db import transaction

from shapes.rectangle import Rectangle
from signals_demo import signals
from signals_demo.models import AuditLog, Item


class Command(BaseCommand):
    help = "Prints evidence for the Django signal questions and the Rectangle class."

    def handle(self, *args, **opts):
        out = self.stdout.write
        out("Q1: synchronous or asynchronous?")
        t = time.monotonic()
        Item.objects.create(name="q1")
        out(f"  save() took {time.monotonic() - t:.1f}s; the handler sleeps 2s -> synchronous")

        out("Q2: same thread?")
        Item.objects.create(name="q2")
        out(f"  caller thread={threading.get_ident()} handler thread={signals.observed['handler_thread']}")

        out("Q3: same transaction?")
        try:
            with transaction.atomic():
                Item.objects.create(name="q3")
                raise RuntimeError("rollback")
        except RuntimeError:
            pass
        out(f"  handler saw in_atomic_block={signals.observed['in_atomic_block']}")
        out(f"  after rollback, AuditLog rows for q3: {AuditLog.objects.filter(message='saved q3').count()} -> same transaction")

        out(f"Rectangle(5, 3) iterates as: {list(Rectangle(5, 3))}")
