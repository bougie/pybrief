from django import forms
from .models import Tag, Post


class TagWidget(forms.TextInput):
    """TagField displayer"""

    def render(self, name, value, attrs=None):
        """Parse and replace input content before rendering it.
        :param name: name of input field
        :param value: list of Tags pk
        :param attrs:

        This function changes Tag.pk into Tag.name"""

        if isinstance(value, list):
            value = ', '.join(_.name for _ in Tag.objects.filter(pk__in=value))
        return super(TagWidget, self).render(name, value, attrs)


class TagField(forms.CharField):
    """Handle Tags in a form"""

    widget = TagWidget

    def clean(self, value):
        return super(TagField, self).clean(value)


class MarkdownField(forms.CharField):
    """Handle markdown input in a form"""

    widget = forms.Textarea()

    def clean(self, value):
        return super(MarkdownField, self).clean(value)


class PostForm(forms.ModelForm):
    """Handle post creation"""

    # Override tags form field with a tag field
    tags = TagField(max_length=255, required=False)
    # Override content form field
    content = MarkdownField()

    class Meta:
        model = Post
        fields = ['title', 'author', 'create_date', 'content', 'parser', 'tags',
                  'filename']

    def save(self, commit=True, no_save_file=False):
        """Save the new (or modified) post.

        :param commit: commit or not the result
        :param no_save_file: do not generate and save post file on disk"""

        instance = forms.ModelForm.save(self, commit=False)

        def save_m2m():
            """Handle the m2m relation between Post and Tags. This function
            will erase and add tags for every actions on a post."""

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
            instance.save(no_save_file=no_save_file)
            self.save_m2m()

        return instance
