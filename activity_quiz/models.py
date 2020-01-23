import uuid

from django.db import models

from course_app.models import Activity, Solution

from polymorphic.models import PolymorphicModel
from django.contrib.postgres.fields import JSONField


class ActivityQuiz(Activity):
    fa_icon = "fas fa-tasks"
    completable = True

    max_attempts = models.PositiveIntegerField(null=False, default=1)

    timelimit = models.PositiveIntegerField(null=False, default=0)


class Question(PolymorphicModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    activity = models.ForeignKey(ActivityQuiz, on_delete=models.CASCADE)

    # question text
    text = models.TextField(null=False, blank=False)

    # option question hint for 1/2 of score
    hint = models.TextField(null=True, blank=True)

    # optional full solution to question
    solution = models.TextField(null=True, blank=True)

    # order among given quiz questions
    order = models.PositiveIntegerField(default=0, editable=True, db_index=True)

    # shuffle question answers
    shuffle = models.BooleanField(null=False, default=False, choices=((True, 'YES'), (False, 'NO')))

    class Meta:  # noqa
        ordering = ['order']

    def save(self, *args, **kwargs):
        # cast empty strings to NULL
        self.hint = self.hint or None
        self.solution = self.solution or None
        super().save(*args, **kwargs)

    def question_type(self):
        return self.__class__.__name__


class SingleChoiceQuestion(Question):
    template = 'activity_quiz/questions/single_choice_question.html'


class SingleChoiceAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    question = models.ForeignKey(SingleChoiceQuestion, related_name='answers_set', on_delete=models.CASCADE)

    text = models.TextField(null=False, blank=False)
    correct = models.BooleanField(null=False)

    order = models.PositiveIntegerField(default=0, editable=True, db_index=True)

    class Meta:  # noqa
        ordering = ['order']


class MultipleChoiceQuestion(Question):
    template = 'activity_quiz/questions/multiple_choice_question.html'


class MultipleChoiceAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    question = models.ForeignKey(MultipleChoiceQuestion, related_name='answers_set', on_delete=models.CASCADE)

    text = models.TextField(null=False, blank=False)
    score = models.IntegerField(null=False, default=0)

    order = models.PositiveIntegerField(default=0, editable=True, db_index=True)

    class Meta:  # noqa
        ordering = ['order']


class OpenQuestion(Question):
    template = 'activity_quiz/questions/open_question.html'

    placeholder = models.CharField(null=True, blank=True, max_length=32)


class OpenAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    question = models.ForeignKey(OpenQuestion, related_name='answers_set', on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=False)


class SolutionQuiz(Solution):
    attempt = models.PositiveIntegerField(default=0, null=False)
    started_at = models.DateTimeField(auto_now_add=True, null=False)

    answers = JSONField()

    # def set_progress(self, user, question, value):
    #     pass
    # ZWPA: Database Session State


    # class Meta:  # noqa
    #     unique_together = ('activity_id', 'user_id', 'attempt')
