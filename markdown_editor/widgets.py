import json
from typing import List
from django.forms.widgets import Textarea
from django.forms import Media


class AdminMarkdownWidget(Textarea):
    """
    Widget providing simple wrapper for textareas with markdown editor.

    It doesn't use 3rd party javascript library to render markdown,
    but it use provided endpoint url for server side rendering (to be consistent
    among different views).
    """

    @property
    def media(self):
        return Media(
            css={
                'all': (
                    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css',
                    'markdown_editor/css/style.css'
                ),
            },
            js=('markdown_editor/javascript/editor.js',)
        )

    def __init__(self, *args, preview_url: str = '/markdown/', toolbar: List[str] = None, **kwargs):
        super().__init__(attrs=dict(rows=5), *args, **kwargs)  # NOTE: default value rows = 10 is too much

        if not isinstance(preview_url, str):
            raise TypeError('preview_url must contain string url')
        self.preview_url = preview_url

        if not (toolbar is None or (isinstance(toolbar, list) and all(isinstance(item, str) for item in toolbar))):
            raise TypeError('toolbar must be None or list of button names (see: editor.js)')
        self.toolbar = toolbar

    def render(self, name, value, attrs=None, renderer=None):
        textarea = super().render(name, value, attrs, renderer)

        initializers = """
            <style type="text/css">.field-%(name)s {overflow: visible;}</style>

            <script>
                (function(){
                  new MarkdownEditor('%(element_id)s', {
                    'url': '%(preview_url)s',
                    'toolbar': %(toolbar)s
                  });
                })();
            </script>
        """ % dict(name=name, element_id=attrs['id'], preview_url=self.preview_url, toolbar=json.dumps(self.toolbar))

        return textarea + initializers
