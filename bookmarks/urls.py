from django.conf.urls import patterns, url
from .views import LinkList

urlpatterns = patterns(
    '',
    url(r'^$', LinkList.as_view(), name='bookmarks_index'),
    url(r'^new$', 'bookmarks.views.add_link', name='bookmarks_add'),
)
