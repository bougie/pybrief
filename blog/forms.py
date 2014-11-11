from django import forms
from .models import Tag


class TagWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if isinstance(value, list):
            value = ', '.join(_.name for _ in Tag.objects.filter(pk__in=value))
        return super(TagWidget, self).render(name, value, attrs)


class TagField(forms.CharField):
    widget = TagWidget

    def clean(self, value):
        value = super(TagField, self).clean(value)
        return value


class PostForm(forms.ModelForm):
    tags = TagField(max_length=255, required=False)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, commit=False)

        def save_m2m():
            instance.tags.clear()
            for tagname in self.cleaned_data['tags'].split(','):
                tagname = tagname.lower().strip()
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
