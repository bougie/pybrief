from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'blog.views.index', name='blog_index'),
    url(r'^([0-9]*)/(.*)$', 'blog.views.show_post', name='blog_post'),
    url(r'^tag/(.*)$', 'blog.views.show_posts_by_tag', name='blog_posts_tag'),
    url(r'^author/(.*)$', 'blog.views.show_posts_by_author',
        name='blog_posts_author'),
    url(r'^archives/([0-9]{4})$', 'blog.views.show_posts_by_date',
        name='blog_posts_archives'),
    url(r'^archives/([0-9]{4})/([0-9]{1,2})$', 'blog.views.show_posts_by_date',
        name='blog_posts_archives'),
)
