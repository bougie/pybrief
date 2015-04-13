from django.conf import settings


def global_vars(request):
    """Set global vars for templates"""

    tplvars = {}

    try:
        curr_mod = request.path.split('/')[1]
        if curr_mod == '/' or len(curr_mod.strip()) == 0:
            curr_mod = 'index'
        tplvars['nav_current_module'] = curr_mod
    except:
        tplvars['nav_current_module'] = 'index'

    items = ['BLOG_TITLE', 'BLOG_SUBTITLE', 'BLOG_AUTHOR', 'BLOG_DESCRIPTION',
             'BLOG_KEYWORDS']
    for item in items:
        tplvars[item] = getattr(settings, item, None)

    return tplvars
