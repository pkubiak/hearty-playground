import os
import uuid
import random
from functools import cached_property

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from polymorphic.models import PolymorphicModel


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


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    order = models.PositiveIntegerField(default=0, editable=True, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} / {self.title}"


class Activity(PolymorphicModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255, null=False, blank=False)

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    # Order field for SortableMixin
    order = models.PositiveIntegerField(default=0, editable=True, db_index=True)

    # Related content_type data
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=False)
    # object_id = models.PositiveIntegerField(null=False)
    # content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Activities'
        # unique_together = ('content_type', 'object_id')

    # def clean(self):
        # print('*'*100)
        # print(self.object_id, self.title)#, self.content_type)
        # print('*'*100)
        # if self.content_object is None:
        #     raise ValidationError('Related activity content object does not exists')
        # if not isinstance(self.content_object, ActivityContent):
        #     raise ValidationError('Related activity content does not inherits from ActivityContent base class')

    # @property
    # def fa_icon(self) -> str:
    #     return ''
    #     # return self.content_type.model_class().fa_icon
    #
    # @property
    # def completable(self):
    #     """Control if given activity require any actions to be completed."""
    #     return False
    #     # return self.content_object.completable
#
#
# class ActivityContent(models.Model):
#     """Base class for Activity extended content."""
#     activity = GenericRelation(Activity)
#
#     class Meta:
#         abstract = True
