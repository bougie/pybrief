from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.shortcuts import render_response
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.views.generic import ListView
from django.conf import settings
from .models import Post, Tag


def index(request):
    """Blog home page. Render the posts list"""

    dates = Post.objects.datetimes('create_date', 'month', order='DESC')

    try:
        paginator = Paginator(
            Post.objects.all().order_by('-create_date'),
            settings.NB_FULL_POSTS)
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
                                   {'posts': posts, 'tags': tags,
                                    'dates': dates})


def show_post(request, postid, postslug=None):
    """Display a post for a given id

    :param postid: post numerical id
    :type postid: int
    :param postslug: post slug
    :type postslug: str"""

    # Check if post exists and if the URL is well formated
    try:
        post = Post.objects.get(id=postid)
    except Post.DoesNotExist:
        raise Http404
    else:
        if postslug is None or post.slug != postslug:
            return redirect(reverse('blog_post', args=[post.id, post.slug]),
                            permanent=True)

    return render_response(request, 'blog/show_post.tpl', {'post': post})


class PostList(ListView):
    """List posts for a given filter paste in URL"""

    context_object_name = 'posts'
    template_name = 'blog/post_list.tpl'
    paginate_by = settings.NB_POSTS

    def get_queryset(self):
        sub = self.kwargs['submodule']
        if sub == 'tag':
            tag = Tag.objects.get(name=self.kwargs['tagname'])
            return Post.objects.all().filter(tags=tag).order_by('-create_date')
        elif sub == 'author':
            return Post.objects.filter(
                author=self.kwargs['author']).order_by('-create_date')
        elif sub == 'archives':
            year = self.kwargs.get('year', None)
            month = self.kwargs.get('month', None)
            if month is not None:
                return Post.objects.filter(
                    create_date__year=year,
                    create_date__month=month).order_by('-create_date')
            else:
                return Post.objects.filter(
                    create_date__year=year).order_by('-create_date')
        else:
            return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def render_to_response(self, context, **response_kwargs):
        return render_response(self.request, self.get_template_names(),
                               context, **response_kwargs)
