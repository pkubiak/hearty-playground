import json
from django.forms.widgets import Textarea
from django.forms import Media


class StringArrayWidget(Textarea):
    """
    Widget for managing array of strings with tagify JS pluggin.

    @see: https://github.com/yairEO/tagify
    """

    @property
    def media(self):
        return Media(
            css={
                'all': ('course_app/css/tagify.css',),
            },
            js=('course_app/javascript/tagify.js',)
        )

    def render(self, name, value, attrs=None, renderer=None):
        textarea = super().render(name, value, attrs, renderer)

        initializer = "<script>(function(){new Tagify(document.getElementById('id_%s'), {editTags: 1});})();</script>" % (name,)

        return textarea + initializer

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)

        if not value:
            return None

        try:
            raw_values = json.loads(value)
            if isinstance(raw_values, list):
                values = [item['value'] for item in raw_values]
                return values
        except json.JSONDecodeError:
            return super().value_from_datadict(data, files, name)

        return None
