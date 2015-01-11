from core.shortcuts import render_response
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
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


@require_http_methods(["GET", "POST"])
def form_link(request, linkid=None):
    """Add or edit a link"""

    if request.method == "POST":
        try:
            if linkid is not None:
                form = LinkForm(request.POST,
                                instance=Link.objects.get(id=linkid))
            else:
                form = LinkForm(request.POST)

            if form.is_valid():
                form.save()
        except Exception as e:
            return HttpResponse(status=500)
        else:
            return HttpResponseRedirect(reverse('bookmarks_index'))
    elif request.method == "GET" and request.is_ajax():
        try:
            link = Link.objects.get(id=linkid)
        except Link.DoesNotExist:
            return HttpResponse(status=404)
        except:
            return HttpResponse(status=500)
        else:
            return JsonResponse({
                'form_action': reverse('bookmarks_edit', args=[linkid]),
                'form_method': 'POST',
                'link': {
                    'url': link.url,
                    'name': link.name,
                    'tags': ','.join([_.name for _ in link.tags.all()])
                }
            })
    else:
        return HttpResponse(status=405)
