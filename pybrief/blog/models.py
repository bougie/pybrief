import os
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from .utils import save_post_file, md5sum, wrap_description
try:
    from markdown2 import markdown
except:
    markdown = None
from core.models import Tag


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
    filename = models.TextField(blank=True, null=True, default=None)

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

        if self.filename is None or len(self.filename.strip()) == 0:
            # It's a new post created from the admin area
            self.filename = os.path.join(settings.BASE_DIR,
                                         'data',
                                         '%s.bp' % (self.slug,))
        else:
            # It's a post imported (new or update) from an existing file
            # or it's a post updated from the admin area
            try:
                post = Post.objects.get(filename=self.filename)
                self.pk = post.pk
                self.hash = post.hash
            except Post.DoesNotExist:
                self.pk = None
                self.hash = None
            except Post.MultipleObjectsReturned:
                raise ValueError(
                    "Error while retrieving primary key value for the update")

        do_save = True
        if ('no_save_file' in kwargs and kwargs['no_save_file'] is False
                or 'no_save_file' not in kwargs):
            # Save the post file only if it's edition from the admin area. In
            # this cas, no_save_file will not exist or it's value will be False.
            self.hash = save_post_file(filename=self.filename,
                                       title=self.title,
                                       author=self.author,
                                       date=self.create_date,
                                       content=self.content,
                                       parser=self.parser)

            # when importing from file, save the post in DB when it content has
            # changed (hash is different)
            if self.hash is None or self.hash != md5sum(self.filename):
                do_save = True
            else:
                do_save = False

        if do_save:
            if 'no_save_file' in kwargs:
                del kwargs['no_save_file']
            super(Post, self).save(*args, **kwargs)
