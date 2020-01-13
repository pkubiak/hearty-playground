import os
import uuid
import random
from functools import cached_property

from django.db import models
from django.contrib.postgres.fields import ArrayField

from adminsortable.models import SortableMixin, SortableForeignKey


def course_directory_path(instance, filename):
    _, ext = os.path.splitext(filename)

    if not (instance.id and ext in {'.jpg', '.png'}):
        raise ValueError("Can't upload given file")

    return os.path.join('course_app', 'course', str(instance.id), f"banner{ext}")


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=False, blank=False, unique=True)

    banner = models.ImageField(upload_to=course_directory_path, null=True, blank=True)

    description = models.TextField(null=False, blank=True)
    keywords = ArrayField(models.CharField(max_length=32), null=True, blank=True)

    # TODO: add field available_from / available_to (datarange)

    def last_user_activity(self, user):
        return None  # TODO: implement

    @cached_property
    def user_progress(self, user=None) -> float:
        """Percentage of this course completation."""
        val = 200 * random.random() - 100.0  # FIXME: return something more relevant
        if val <= 0.0:
            return None
        return val

    def __str__(self):
        return f"{self.title} ({self.id})"


class Lesson(SortableMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    course = SortableForeignKey(Course, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} / {self.title}"
