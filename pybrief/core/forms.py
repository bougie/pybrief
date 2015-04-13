from django import forms
from .models import Tag


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
