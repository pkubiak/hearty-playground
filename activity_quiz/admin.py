from django.contrib import admin
from .models import ActivityQuiz
from course_app.admin import ActivityChildAdmin


@admin.register(ActivityQuiz)
class ActivtyQuizAdmin(ActivityChildAdmin):
    base_model = ActivityQuiz
