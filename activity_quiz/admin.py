from django.db import models
from django.contrib import admin

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from adminsortable2.admin import SortableInlineAdminMixin
from markdown_editor.widgets import AdminMarkdownWidget

from course_app.admin import ActivityChildAdmin
from .models import ActivityQuiz, Question, SingleChoiceQuestion, SingleChoiceAnswer, MultipleChoiceQuestion, MultipleChoiceAnswer, OpenQuestion, OpenAnswer


class QuestionInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Question
    show_change_link = True
    extra = 0

    # def has_change_permission(self, request, obj):
    #     return False


@admin.register(ActivityQuiz)
class ActivityQuizAdmin(ActivityChildAdmin):
    base_model = ActivityQuiz
    inlines = [QuestionInline]

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownWidget},
    }


@admin.register(Question)
class QuestionAdmin(PolymorphicParentModelAdmin):
    base_model = Question
    list_filter = (PolymorphicChildModelFilter,)
    list_display = ('__str__', 'activity', 'text',)

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownWidget},
    }

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

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownWidget},
    }


class MultipleChoiceAnswerInline(SortableInlineAdminMixin, admin.TabularInline):
    model = MultipleChoiceAnswer


@admin.register(MultipleChoiceQuestion)
class MultipleChoiceQuestionAdmin(QuestionChildAdmin):
    base_model = MultipleChoiceQuestion
    inlines = [MultipleChoiceAnswerInline]


class OpenAnswerInline(admin.TabularInline):
    model = OpenAnswer


@admin.register(OpenQuestion)
class OpenQuestionAdmin(QuestionChildAdmin):
    base_model = OpenQuestion
    inlines = [OpenAnswerInline]
