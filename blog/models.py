from django.db import models


class Tag(models.Model):
    """Post's tags"""

    name = models.CharField(max_length=255)


class Post(models.Model):
    """Blog post"""

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now=True)
    content = models.TextField()
    parser = models.CharField(max_length=30, blank=True, null=True)
    description_html = models.CharField(max_length=255, blank=True, null=True)
    content_html = models.TextField(blank=True, null=True)

    tags = models.ManyToManyField(Tag, null=True)
