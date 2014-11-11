from django.db import models


class Tag(models.Model):
    """Post's tags"""

    name = models.CharField(max_length=255)


class Post(models.Model):
    """Blog post"""

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    content = models.TextField()

    tags = models.ManyToManyField(Tag, null=True)
