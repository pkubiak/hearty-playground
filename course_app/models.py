from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=False, blank=False, unique=True)

    description = models.TextField(null=False, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)
