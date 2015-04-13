from django.contrib import admin
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    """Admin class for managing tags in the admin area"""

    list_display = ('name',)

admin.site.register(Tag, TagAdmin)
