from django import template

register = template.Library()


@register.filter
def truncatelink(link, trunc_len=69):
    try:
        trunc_len = int(trunc_len)
    except:
        trunc_len = 69

    if len(link) > trunc_len:
        delta = int(0.33 * trunc_len)
        link = '%s[...]%s' % (link[:trunc_len - delta - 5], link[-delta:])

    return link
