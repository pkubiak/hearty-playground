from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from .models import Course
from .widgets import StringArrayWidget
from django.utils.html import format_html


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('banner_img', 'title', 'description', 'keywords')
    list_display_links = ('title', )
    ordering = ('title', )

    formfield_overrides = {
        ArrayField: {'widget': StringArrayWidget},
    }

    def banner_img(self, instance):
        """Display banner as clickable image tag."""
        if instance.banner:
            return format_html('<a href="%s"><img src="%s" style="max-width:160px;max-height:120px"/></a>' % (instance.banner.url, instance.banner.url))
        return None

    banner_img.short_description = 'Banner'
    banner_img.allow_tags = True
