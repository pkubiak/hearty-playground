from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from .models import Course
from .widgets import StringArrayWidget


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'description', 'keywords')
    ordering = ('title', )

    formfield_overrides = {
        ArrayField: {'widget': StringArrayWidget},
    }
