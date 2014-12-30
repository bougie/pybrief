from core.shortcuts import render_response
from django.views.generic import ListView
from .models import Link


class LinkList(ListView):
    """List links"""

    context_object_name = 'links'
    template_name = 'bookmarks/link_list.tpl'

    def get_queryset(self):
        return Link.objects.all()

    def render_to_response(self, context, **response_kwargs):
        return render_response(self.request, self.get_template_names(),
                               context, **response_kwargs)
