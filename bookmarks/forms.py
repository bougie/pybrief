from django import forms
from .models import Link
from core.models import Tag
from core.forms import TagField


class LinkForm(forms.ModelForm):
    """Handle link creation"""

    # Override tags form field with a tag field
    tags = TagField(max_length=255, required=False)

    class Meta:
        model = Link
        fields = ['url', 'name', 'tags']

    def save(self, commit=True):
        """Save the new (or modified) link.

        :param commit: commit or not the result"""

        instance = forms.ModelForm.save(self, commit=False)

        if not instance.url.startswith('http'):
            instance.url = 'http://' + instance.url

        def save_m2m():
            """Handle the m2m relation between Link and Tags. This function
            will erase and add tags for every actions on a link."""

            instance.tags.clear()
            for tagname in self.cleaned_data['tags'].split(','):
                tagname = tagname.lower().strip()
                if len(tagname) > 0:
                    try:
                        tag = Tag.objects.get(name=tagname)
                    except Tag.DoesNotExist:
                        tag = Tag(name=tagname)
                        tag.save()
                    instance.tags.add(tag)
        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance
