from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)


class AuditLog(models.Model):
    """Written by a signal handler; used to inspect transaction behaviour."""
    message = models.CharField(max_length=200)
