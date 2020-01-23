from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.shortcuts import render

import markdown
import frontmatter


@xframe_options_sameorigin
def markdown_preview(request):
    if request.method == 'POST':
        assert 'text' in request.POST

        text = request.POST['text']
        metadata, content = frontmatter.parse(text)

        return render(request, 'playground/markdown_preview.html', {
            'content': content,
            'metadata': metadata
        })
