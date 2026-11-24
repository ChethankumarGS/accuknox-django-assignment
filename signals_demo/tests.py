"""Each test is a runnable proof of one answer. Run: python manage.py test -v 2"""
import threading
import time

from django.db import transaction
from django.test import TestCase, TransactionTestCase

from . import signals
from .models import AuditLog, Item


class Q1SynchronousTest(TestCase):
    def test_signals_are_synchronous_by_default(self):
        """save() only returns after the 2s handler has finished.

        If signals were asynchronous, save() would return almost instantly,
        before the handler finished.
        """
        signals.observed.clear()
        start = time.monotonic()
        Item.objects.create(name="a")
        returned_at = time.monotonic()
        # handler finished BEFORE save() returned -> caller was blocked
        self.assertLessEqual(signals.observed["handler_finished_at"], returned_at)
        self.assertGreaterEqual(returned_at - start, 2.0)


class Q2SameThreadTest(TestCase):
    def test_signals_run_in_callers_thread(self):
        signals.observed.clear()
        caller_thread = threading.get_ident()
        Item.objects.create(name="b")
        self.assertEqual(signals.observed["handler_thread"], caller_thread)


class Q3SameTransactionTest(TransactionTestCase):
    def test_signal_runs_inside_callers_transaction(self):
        """The handler sees an open atomic block, and its write is rolled back
        together with the caller's write when the caller's transaction fails."""
        signals.observed.clear()
        try:
            with transaction.atomic():
                Item.objects.create(name="c")
                self.assertTrue(signals.observed["in_atomic_block"])
                self.assertEqual(AuditLog.objects.count(), 1)  # visible inside
                raise RuntimeError("force rollback")
        except RuntimeError:
            pass
        # Both the Item and the AuditLog row created by the signal are gone,
        # so the handler shared the caller's transaction.
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(AuditLog.objects.count(), 0)
