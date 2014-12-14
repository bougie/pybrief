from django.conf.urls import patterns, url
from .views import PostList

urlpatterns = patterns(
    '',
    url(r'^$', 'blog.views.index', name='blog_index'),
    url(r'^([0-9]*)/(.*)$', 'blog.views.show_post', name='blog_post'),
    url(r'^tag/(?P<tagname>.*)$',
        PostList.as_view(), {'submodule': 'tag'},
        name='blog_posts_tag'),
    url(r'^author/(?P<author>.*)$',
        PostList.as_view(), {'submodule': 'author'},
        name='blog_posts_author'),
    url(r'^archives/(?P<year>[0-9]{4})$',
        PostList.as_view(), {'submodule': 'archives'},
        name='blog_posts_archives'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})$',
        PostList.as_view(), {'submodule': 'archives'},
        name='blog_posts_archives'),
)
