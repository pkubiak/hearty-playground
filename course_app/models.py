import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


#
# def course_upload_path(instance, ):
#     pass


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=False, blank=False, unique=True)

    # banner = models.FileField(upload_to=user_directory_path)

    description = models.TextField(null=False, blank=True)
    keywords = ArrayField(models.CharField(max_length=32), null=True, blank=True)
