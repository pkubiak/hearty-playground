from django import template
register = template.Library()


@register.filter
def at_index(indexable, i):
    if indexable is None or i is None:
        return None
    return indexable[i]