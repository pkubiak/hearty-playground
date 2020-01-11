from django.contrib import admin
from django.db import models

from .models import Article

from markdown_editor.widgets import AdminMarkdownWidget


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('order', 'title', 'slug')
    ordering = ('order', 'slug',)

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownWidget},
    }
