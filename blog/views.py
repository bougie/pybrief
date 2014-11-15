from django.shortcuts import render_to_response
from .models import Post, Tag


def index(request):
    """Blog home page. Render the posts list"""

    posts = Post.objects.all().order_by('-create_date')
    tags = Tag.objects.all()

    return render_to_response('blog/index.tpl', {'posts': posts, 'tags': tags})
