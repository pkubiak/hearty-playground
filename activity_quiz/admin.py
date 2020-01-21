from django.contrib import admin
from .models import ActivityQuiz, Question, SingleChoiceQuestion, SingleChoiceAnswer
from course_app.admin import ActivityChildAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from adminsortable2.admin import SortableInlineAdminMixin


@admin.register(ActivityQuiz)
class ActivtyQuizAdmin(ActivityChildAdmin):
    base_model = ActivityQuiz


@admin.register(Question)
class QuestionAdmin(PolymorphicParentModelAdmin):
    base_model = Question
    list_filter = (PolymorphicChildModelFilter,)

    def get_child_models(self):
        return Question.__subclasses__()


class QuestionChildAdmin(PolymorphicChildModelAdmin):
    base_model = Question


class SingleChoiceAnswerInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SingleChoiceAnswer


@admin.register(SingleChoiceQuestion)
class SingleChoiceQuestionAdmin(QuestionChildAdmin):
    base_model = SingleChoiceQuestion
    inlines = [SingleChoiceAnswerInline]
