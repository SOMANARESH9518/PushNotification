from __future__ import unicode_literals

from django.db import models


class GCMStore(models.Model):
    gcmId = models.CharField(unique=True, null=False, max_length=200)
