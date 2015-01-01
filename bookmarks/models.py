from django.db import models
from core.models import Tag
from .utils import get_title_link, get_domain_link


class Link(models.Model):
    """Bookmark link representation"""

    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.TextField()
    domain = models.CharField(max_length=255, blank=True, null=True)
    insert_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, null=True)

    def save(self, *args, **kwargs):
        self.title = get_title_link(url=self.url)
        self.domain = get_domain_link(url=self.url)

        super(Link, self).save(args, kwargs)
