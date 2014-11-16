from core.shortcuts import render_response


def index(request):
    return render_response(request, 'core/index.tpl', {'posts': []})
