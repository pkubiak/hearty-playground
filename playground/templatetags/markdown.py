import markdown as md

from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter
@mark_safe
def markdown(value, arg=None):
    return md.markdown(value, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.admonition',
        'pymdownx.mark',
        'pymdownx.tasklist',
        'pymdownx.caret',
        'pymdownx.tilde',
    ])
