from django.db import models


class Tag(models.Model):
    """Item's tags"""

    name = models.CharField(max_length=255)
