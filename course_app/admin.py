from django.contrib import admin
from django.forms import widgets

from .models import Course
from django.contrib.postgres.fields import ArrayField
from .widgets import SplitTextWidget


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    # list_display = ('order', 'title', 'slug')
    # ordering = ('order', 'slug',)

    formfield_overrides = {
        ArrayField: {'widget': SplitTextWidget},
    }
