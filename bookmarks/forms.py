from django import forms
from .models import Link
from core.forms import TagField


class LinkForm(forms.ModelForm):
    """Handle link creation"""

    # Override tags form field with a tag field
    tags = TagField(max_length=255, required=False)

    class Meta:
        model = Link
        fields = ['name', 'url', 'tags']
