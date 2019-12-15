import markdown
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)

    slug = models.SlugField(max_length=100, null=False, blank=False,
                            unique=True)

    order = models.IntegerField(blank=False, default=1000)

    content = models.TextField(null=False, blank=False)

    def content_html(self):
        """Return `self.content` parsed as markdown to HTML."""
        print(markdown.markdown(self.content))
        return markdown.markdown(self.content)
