from django.shortcuts import render_to_response
from .models import Post, Tag


def index(request):
    """Blog home page. Render the posts list"""

    posts = Post.objects.all().order_by('-create_date')
    tags = Tag.objects.all()

    return render_to_response('blog/index.tpl', {'posts': posts, 'tags': tags})


def show_posts_by_tag(request, tagname):
    """List posts for a given tag

    :param tagname: the name of the tag
    :type tagname: str"""

    posts = Post.objects.all().order_by('-create_date')

    return render_to_response('blog/posts_by_tag.tpl', {'posts': posts})
