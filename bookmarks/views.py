from core.shortcuts import render_response
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from core.models import Tag
from .models import Link
from .forms import LinkForm


class LinkList(ListView):
    """List links"""

    context_object_name = 'links'
    template_name = 'bookmarks/link_list.tpl'
    paginate_by = settings.NB_LINKS

    def get_queryset(self):
        sub = self.kwargs.get('submodule', None)
        if sub == 'tag':
            tag = Tag.objects.get(name=self.kwargs['tagname'])
            return Link.objects.all().filter(tags=tag)
        else:
            return Link.objects.all()

    def get_context_data(self, **kwargs):
        context = super(LinkList, self).get_context_data(**kwargs)

        context['tags'] = Tag.objects.all()
        context['form'] = LinkForm()

        return context

    def render_to_response(self, context, **response_kwargs):
        return render_response(self.request, self.get_template_names(),
                               context, **response_kwargs)


@require_http_methods(["POST"])
def add_link(request):
    form = LinkForm(request.POST)
    try:
        if form.is_valid():
            form.save()
    except:
        pass
    finally:
        return HttpResponseRedirect(reverse('bookmarks_index'))
