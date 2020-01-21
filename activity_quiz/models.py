import uuid

from django.db import models

from course_app.models import Activity

from polymorphic.models import PolymorphicModel


class ActivityQuiz(Activity):
    fa_icon = "fas fa-tasks"
    
    max_attempts = models.PositiveIntegerField(default=1)


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
    pass


class SingleChoiceAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    question = models.ForeignKey(SingleChoiceQuestion, related_name='answers_set', on_delete=models.CASCADE)

    text = models.TextField(null=False, blank=False)
    correct = models.BooleanField(null=False)

    order = models.PositiveIntegerField(default=0, editable=True, db_index=True)

    class Meta:
        ordering = ['order']


class MultipleChoiceQuestion(Question):
    pass


class MultipleChoiceAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    question = models.ForeignKey(MultipleChoiceQuestion, related_name='answers_set', on_delete=models.CASCADE)

    text = models.TextField(null=False, blank=False)
    score = models.IntegerField(null=False, default=0)

    order = models.PositiveIntegerField(default=0, editable=True, db_index=True)

    class Meta:
        ordering = ['order']


# class OpenAnswerQuestion(Question):
#     pass
