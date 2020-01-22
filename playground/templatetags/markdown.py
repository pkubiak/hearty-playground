import markdown as md

from django import template

register = template.Library()


@register.filter
def markdown(value, arg):
    return md.markdown(value, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.admonition',
        'pymdownx.mark',
        'pymdownx.tasklist',
        'pymdownx.caret',
        'pymdownx.tilde',
    ])
