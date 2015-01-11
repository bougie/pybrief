from django.conf.urls import patterns, url
from .views import LinkList

urlpatterns = patterns(
    '',
    url(r'^$', LinkList.as_view(), name='bookmarks_index'),
    url(r'^new$', 'bookmarks.views.form_link', name='bookmarks_add'),
    url(r'^edit/([0-9]+)$', 'bookmarks.views.form_link', name='bookmarks_edit'),
    url(r'^tag/(?P<tagname>.*)$',
        LinkList.as_view(), {'submodule': 'tag'},
        name='bookmarks_links_tag'),
)
