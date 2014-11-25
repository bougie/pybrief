from django.contrib import admin
from .models import Post, Tag
from .forms import PostForm


class PostAdmin(admin.ModelAdmin):
    """Admin class for managing blog posts in the admin area"""

    form = PostForm
    fields = PostForm.Meta.fields
    list_display = ('title', 'slug', 'author', 'filename', 'create_date',
                    'parser')


class TagAdmin(admin.ModelAdmin):
    """Admin class for managing tags in the admin area"""

    list_display = ('name',)

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
