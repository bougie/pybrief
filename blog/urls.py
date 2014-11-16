from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'blog.views.index', name='blog_index'),
    url(r'^tag/(.*)$', 'blog.views.show_posts_by_tag', name='blog_posts_tag'),
)
