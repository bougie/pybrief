from django.contrib import admin
from .models import Link
from .forms import LinkForm


class LinkAdmin(admin.ModelAdmin):
    """Admin class for managing bookmark links in the admin area"""

    form = LinkForm
    fields = LinkForm.Meta.fields
    list_display = ('name', 'url')

admin.site.register(Link, LinkAdmin)
