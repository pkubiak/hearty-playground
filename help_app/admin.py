from django.contrib import admin
from django.db import models

from .models import Article

from markdown_editor.widgets import AdminMarkdownWidget
from adminsortable2.admin import SortableAdminMixin


@admin.register(Article)
class ArticleAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('order', 'title', 'slug')
    list_display_links = ('title',)

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownWidget},
    }
