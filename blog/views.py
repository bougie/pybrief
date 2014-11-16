from django.shortcuts import redirect
from core.shortcuts import render_response
from django.core.urlresolvers import reverse
from django.http import Http404
from .models import Post, Tag


def index(request):
    """Blog home page. Render the posts list"""

    posts = Post.objects.all().order_by('-create_date')
    tags = Tag.objects.all()

    return render_response(request,
                           'blog/index.tpl',
                           {'posts': posts, 'tags': tags})


def show_post(request, postid, postslug=None):
    """Show post for a given id.

    :param postid: numerical id of the post
    :type postid: int
    :param postslug: slug of the post
    :type postslug: str"""

    #
    # Check if post exists and if the URL is well formated
    #
    try:
        post = Post.objects.get(id=postid)
    except Post.DoesNotExist:
        raise Http404
    else:
        if postslug is None or post.slug != postslug:
            return redirect(reverse('blog_post', args=[post.id, post.slug]),
                            permanent=True)

    return render_response(request, 'blog/show_post.tpl', {'post': post})


def show_posts_by_tag(request, tagname):
    """List posts for a given tag

    :param tagname: the name of the tag
    :type tagname: str"""

    posts = Post.objects.all().order_by('-create_date')

    return render_response(request, 'blog/posts_by_tag.tpl', {'posts': posts})
