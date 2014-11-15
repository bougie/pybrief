from django.shortcuts import render_to_response
from .models import Post


def index(request):
    """Blog home page. Render the posts list"""

    posts = Post.objects.all().order_by('-create_date')

    return render_to_response('blog/index.tpl', {'posts': posts})
