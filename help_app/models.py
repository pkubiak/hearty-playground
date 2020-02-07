import uuid

from django.db import models


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=100, null=False, blank=False)

    slug = models.SlugField(max_length=100, null=False, blank=False,
                            unique=True)

    order = models.IntegerField(blank=False, default=0)

    content = models.TextField(null=False, blank=False)


    class Meta(object):
        ordering = ('order', )
