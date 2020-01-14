from django.contrib import admin
from .models import ActivityNote
from course_app.admin import ActivityChildAdmin


@admin.register(ActivityNote)
class NoteActivtyAdmin(ActivityChildAdmin):
    base_model = ActivityNote
