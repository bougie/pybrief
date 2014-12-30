from django.db import models
from core.models import Tag


class Link(models.Model):
    """Bookmark link representation"""

    name = models.CharField(max_length=255)
    url = models.TextField()
    tags = models.ManyToManyField(Tag, null=True)
