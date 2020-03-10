import markdown as md

from django import template
from django.utils.html import mark_safe
from bs4 import BeautifulSoup

register = template.Library()


def _append_class(el, class_):
    el['class'] = el.get('class', []) + [class_]


BOOTSTRAP_CONTEXTUAL_CLASSES = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']


@register.filter
@mark_safe
def markdown(value, arg=None):
    html = md.markdown(value, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.admonition',
        'pymdownx.mark',
        'pymdownx.tasklist',
        'pymdownx.caret',
        'pymdownx.tilde',
        'pymdownx.smartsymbols',
        'pymdownx.magiclink',
        'pymdownx.emoji',
        'pymdownx.superfences',
        'pymdownx.highlight',
    ], extension_configs={
        'pymdownx.highlight': {
            'linenums_style': 'pymdownx-inline'
        }
    }, output_format='html5')

    doc = BeautifulSoup(html, 'html5lib')

    # https://getbootstrap.com/docs/4.4/content/tables/#examples
    for table in doc.find_all('table'):
        if 'highlighttable' in table.get('class', []):
            continue
        _append_class(table, 'table')

    # https://getbootstrap.com/docs/4.4/content/tables/#table-head-options
    for thead in doc.find_all('thead'):
        _append_class(thead, 'thead-light')

    # https://getbootstrap.com/docs/4.4/content/typography/#unstyled
    # for ul in doc.select('ul.task-list'):
    #     _append_class(ul, 'list-unstyled')

    for alert in doc.select('div.admonition'):
        classes = [f"alert-{name}" if name in BOOTSTRAP_CONTEXTUAL_CLASSES else name for name in alert['class'] if name != 'admonition']
        alert['class'] = ['alert'] + classes
        for title in alert.select('p.admonition-title'):
            title.name = 'h4'
            title['class'] = ['alert-heading']

    # Add class to all highlighted lines
    for hll in doc.select('span.lineno + span.hll'):
        lineno = hll.previous
        _append_class(lineno, 'lineno-hll')

    return str(doc.body.decode_contents())
