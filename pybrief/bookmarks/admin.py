from django.contrib import admin
from .models import Link
from .forms import LinkForm


class LinkAdmin(admin.ModelAdmin):
    """Admin class for managing bookmark links in the admin area"""

    form = LinkForm
    fields = LinkForm.Meta.fields
    list_display = ('url', 'name', 'title', 'insert_date', 'update_date')

admin.site.register(Link, LinkAdmin)
