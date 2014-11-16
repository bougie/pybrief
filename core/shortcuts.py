from django.shortcuts import render_to_response
from django.template import RequestContext


def render_response(request, *args, **kwargs):
    """Return the response with render_to_response but with setting context to
    `RequestContext` before"""

    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)
