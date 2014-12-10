from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.shortcuts import render_response
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from .models import Post, Tag


def index(request):
    """Blog home page. Render the posts list"""

    try:
        paginator = Paginator(Post.objects.all().order_by('-create_date'), 5)
        tags = Tag.objects.all()
    except:
        return HttpResponse(status=500)
    else:
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        finally:
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

    try:
        tag = Tag.objects.get(name=tagname)
        paginator = Paginator(
            Post.objects.all().filter(tags=tag).order_by('-create_date'),
            5)
    except Tag.DoesNotExist:
        raise Http404
    except:
        return HttpResponse(status=500)
    else:
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        finally:
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
