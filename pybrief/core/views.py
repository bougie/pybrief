from core.shortcuts import render_response
from blog.models import Post
from bookmarks.models import Link


def index(request):
    try:
        latest_post = Post.objects.all().order_by('-create_date')[0]
        recent_posts = Post.objects.all().order_by('-create_date')[1:6]
        recent_links = Link.objects.all().order_by('-update_date')[0:5]
    except IndexError:
        latest_post = None
        recent_posts = None
        recent_links = None

    return render_response(request,
                           'core/index.tpl',
                           {'post': latest_post, 'posts': recent_posts,
                            'links': recent_links})
