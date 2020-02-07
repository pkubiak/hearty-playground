from django.contrib import admin
from .models import ActivityNote
from course_app.admin import ActivityChildAdmin
from markdown_editor.widgets import AdminMarkdownWidget
from django.db import models


@admin.register(ActivityNote)
class NoteActivtyAdmin(ActivityChildAdmin):
    base_model = ActivityNote

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownWidget},
    }
