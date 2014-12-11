from django.shortcuts import redirect
from core.shortcuts import render_response
from django.core.urlresolvers import reverse
from django.http import Http404
from .models import Post, Tag


def index(request):
    """Blog home page. Render the posts list"""

    dates = Post.objects.datetimes('create_date', 'month', order='DESC')

    posts = Post.objects.all().order_by('-create_date')
    tags = Tag.objects.all()

    return render_response(request,
                           'blog/index.tpl',
                           {'posts': posts, 'tags': tags, 'dates': dates})


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

    try:
        tag = Tag.objects.get(name=tagname)
    except Tag.DoesNotExist:
        raise Http404
    else:
        posts = Post.objects.all().filter(tags=tag).order_by('-create_date')

        return render_response(request,
                               'blog/posts_by_tag.tpl',
                               {'posts': posts})


def show_posts_by_author(request, author):
    """List posts for a given author

    :param tagname: the name of the author
    :type tagname: str"""

    try:
        posts = Post.objects.filter(author=author).order_by('-create_date')
    except Post.DoesNotExist:
        raise Http404
    else:
        return render_response(request,
                               'blog/posts_by_author.tpl',
                               {'posts': posts})


def show_posts_by_date(request, year, month=None):
    """List posts for a given date

    :param year: year of the date
    :type year: str
    :param month: month of the date
    :type month: str"""

    try:
        if month is not None:
            posts = Post.objects.filter(
                create_date__year=year,
                create_date__month=month).order_by('-create_date')
        else:
            posts = Post.objects.filter(
                create_date__year=year).order_by('-create_date')
    except Post.DoesNotExist:
        raise Http404
    else:
        return render_response(request,
                               'blog/posts_by_date.tpl',
                               {'posts': posts})
