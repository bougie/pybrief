import os
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from .utils import save_post_file, md5sum, wrap_description
try:
    from markdown2 import markdown
except:
    markdown = None
import logging


class Tag(models.Model):
    """Post's tags"""

    name = models.CharField(max_length=255)


class Post(models.Model):
    """Blog post"""

    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True, default=None)
    author = models.CharField(max_length=255)
    create_date = models.DateTimeField(blank=True, null=True)
    content = models.TextField()
    parser = models.CharField(max_length=30, blank=True, null=True)
    description_html = models.CharField(max_length=255, blank=True, null=True)
    content_html = models.TextField(blank=True, null=True)
    hash = models.TextField(null=True, default=None)
    filename = models.TextField(null=True, default=None)

    tags = models.ManyToManyField(Tag, null=True)

    def clean(self):
        try:
            if markdown is not None:
                extras = ['fenced-code-blocks']
                self.content_html = markdown(self.content, extras=extras)
                self.description_html = markdown(wrap_description(self.content),
                                                 extras=extras)
        except:
            raise self.ValidationError("Player42, try again")

        super(Post, self).clean()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        if self.filename is None:
            self.filename = os.path.join(settings.BASE_DIR,
                                         'data',
                                         '%s.bp' % (self.slug,))

        logging.debug("Post model filename %s" % (self.filename,))
        logging.debug("Post model pk %s" % (self.pk,))

        if self.pk is None and os.path.exists(self.filename):
            # It's post imported from a existing file
            self.hash = md5sum(self.filename)
        else:
            # New post from admin area or an update
            self.hash = save_post_file(filename=self.filename,
                                       title=self.title,
                                       author=self.author,
                                       date=self.create_date,
                                       content=self.content,
                                       parser=self.parser)
        super(Post, self).save(*args, **kwargs)
