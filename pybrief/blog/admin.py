from django.contrib import admin
from .models import Post
from .forms import PostForm


class PostAdmin(admin.ModelAdmin):
    """Admin class for managing blog posts in the admin area"""

    form = PostForm
    fields = PostForm.Meta.fields
    list_display = ('title', 'slug', 'author', 'filename', 'create_date',
                    'parser')

admin.site.register(Post, PostAdmin)
