from django.contrib import admin
from django.db import models
from django.forms import TextInput

from django.contrib.postgres.fields import ArrayField
from .models import Course, Lesson, Activity
from .widgets import StringArrayWidget
from django.utils.html import format_html
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from adminsortable2.admin import SortableInlineAdminMixin


@admin.register(Activity)
class ActivityAdmin(PolymorphicParentModelAdmin):
    base_model = Activity
    list_display = ('id', 'title', 'lesson', 'order')
    list_filter = (PolymorphicChildModelFilter,)

    def get_child_models(self):
        return Activity.__subclasses__()


class ActivityChildAdmin(PolymorphicChildModelAdmin):
    base_model = Activity


class ActivityInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Activity
    show_change_link = True


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'title')
    list_display_links = ('title',)
    inlines = [ActivityInline]


class LessonInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Lesson
    show_change_link = True

    formfield_overrides = {
        models.TextField: {'widget': TextInput(attrs={'size': 100})},
    }


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('banner_img', 'title', 'description', 'keywords')
    list_display_links = ('title', )
    ordering = ('title', )
    inlines = [LessonInline]

    formfield_overrides = {
        ArrayField: {'widget': StringArrayWidget},
    }

    def banner_img(self, instance):
        """Display banner as clickable image tag."""
        if instance.banner:
            url = instance.banner.url
            return format_html(f'<a href="{url}"><img src="{url}" style="max-width:160px;max-height:120px"/></a>')

        return None

    banner_img.short_description = 'Banner'
    banner_img.allow_tags = True
