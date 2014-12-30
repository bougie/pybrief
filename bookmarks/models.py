from django.db import models
from core.models import Tag


class Link(models.Model):
    """Bookmark link representation"""

    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    url = models.TextField()
    insert_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, null=True)
