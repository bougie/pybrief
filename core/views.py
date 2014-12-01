from core.shortcuts import render_response
from blog.models import Post


def index(request):
    try:
        latest_post = Post.objects.all().order_by('-create_date')[0]
        recent_posts = Post.objects.all().order_by('-create_date')[1:6]
    except IndexError:
        latest_post = None
        recent_posts = None

    return render_response(request,
                           'core/index.tpl',
                           {'post': latest_post, 'posts': recent_posts})
