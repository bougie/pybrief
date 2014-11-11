from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'blog.views.index', name='blog_index'),
)
