def global_vars(request):
    """Set global vars for templates"""

    try:
        curr_mod = request.path.split('/')[1]
        if curr_mod == '/' or len(curr_mod.strip()) == 0:
            curr_mod = 'index'
        return {'nav_current_module': curr_mod}
    except:
        return {'nav_current_module': 'index'}
