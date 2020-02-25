import uuid
import re
from typing import Any, Optional, List
from dataclasses import dataclass
from django.db import models
from functools import cached_property


from course_app.models import Activity, Solution

from polymorphic.models import PolymorphicModel
from django.contrib.postgres.fields import JSONField
from markdown_editor.templatetags.markdown import markdown
from django.core.exceptions import ValidationError


class ActivityQuiz(Activity):
    fa_icon = "fas fa-tasks"
    completable = True

    max_attempts = models.PositiveIntegerField(null=False, default=1)

    timelimit = models.PositiveIntegerField(null=False, default=0)

    # Optional text to show, before user click submit answers
    confirmation_text = models.TextField(null=True, blank=True)

    # Optional text to show, after quiz end
    congratulations = models.TextField(null=True, blank=True)


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

    def serialize_answer(self, request) -> Optional[str]:
        answers = set(request.POST.getlist('answer'))

        for answer in self.answers_set.all():
            if str(answer.id) in answers:
                return str(answer.id)

        return None

    def evaluate_answer(self, saved_answer) -> float:
        if isinstance(saved_answer, str):
            for answer in self.answers_set.all():
                if answer.correct and str(answer.id) == saved_answer:
                    return 1.0

        return 0.0


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

    def serialize_answer(self, request) -> List[str]:
        answers = set(request.POST.getlist('answer'))
        answers_ids = set(map(str, self.answers_set.all().values_list('id', flat=True)))

        return list(answers & answers_ids)

    def evaluate_answer(self, saved_answer: List[str]) -> float:
        if saved_answer is None:
            return 0.0
        if not isinstance(saved_answer, list):
            raise TypeError('Answer should be list')

        max_score = 0
        score = 0
        for answer in self.answers_set.all():
            if answer.score > 0:
                max_score += answer.score
            if str(answer.id) in saved_answer:
                score += answer.score

        return max(score, 0) / max_score


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

    def serialize_answer(self, request):
        answer = request.POST.get('answer')

        if answer is not None:
            answer = str(answer)

        return answer

    def evaluate_answer(self, saved_answer: str) -> float:
        if isinstance(saved_answer, str):
            for answer in self.answers_set.all():
                if answer.text.strip() == saved_answer.strip():
                    return 1.0

        return 0.0


class OpenAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    question = models.ForeignKey(OpenQuestion, related_name='answers_set', on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=False)


class OrderingQuestion(Question):
    template = 'activity_quiz/questions/ordering_question.html'

    GAP_REGEX = r'\[\[(.*?)\]\]'
    MAGIC_UNICODE = '🕊'

    def serialize_answer(self, request):
        answers, used_answers = [], set()
        max_distractor_idx = len(self.all_distractors)

        for i in range(len(self.correct_answers)):
            answer = request.POST.get(f"gap_{i}", '')

            if not re.fullmatch(r'\d+', answer):
                answer = None
            else:
                answer = int(answer)
                if 0 <= answer < len(self.all_distractors) and answer not in used_answers:
                    used_answers.add(answer)
                else:
                    answer = None
            answers.append(answer)

        if all(answer is None for answer in answers):
            return None
        return answers

    def evaluate_answer(self, saved_answers: List[int]) -> float:
        if saved_answers is None:
            return 0.0
        correct = 0

        all_distractors = self.all_distractors
        for answer, correct_answer in zip(saved_answers, self.correct_answers):
            if answer and all_distractors[answer] == correct_answer: # FIXME: IndexError
                correct += 1

        return correct / len(self.correct_answers)

    @property
    def correct_answers(self) -> List[str]:
        """List of gaps answers."""
        return re.findall(self.GAP_REGEX, self.text)

    @property
    def all_distractors(self) -> List[str]:
        """All possible question distractors in some order"""
        distractors = list(self.distractors.all().values_list('text', flat=True))
        return sorted(self.correct_answers + distractors)

    def text_fragments(self):
        text = re.sub(self.GAP_REGEX, self.MAGIC_UNICODE, self.text)
        html = markdown(text)
        return html.split(self.MAGIC_UNICODE)


class OrderingAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    question = models.ForeignKey(OrderingQuestion, related_name='distractors', on_delete=models.CASCADE)

    text = models.TextField(null=False, blank=False)


class SolutionState:
    @dataclass
    class QuestionAnswer:  # noqa
        show_hint: bool = False
        show_solution: bool = False
        answer: Any = None

    @property
    def answers(self):
        return self.solution.answers

    def __init__(self, solution):
        self.solution = solution

    def __getitem__(self, question_uuid):  # noqa
        question_uuid = str(question_uuid)

        if self.answers is None:
            self.answers = {}

        if question_uuid not in self.answers or not isinstance(self.answers[question_uuid], dict):
            self.answers[question_uuid] = dict()
        a = self.answers[question_uuid]

        return SolutionState.QuestionAnswer(
            a.get('show_hint', False),
            a.get('show_solution', False),
            a.get('answer', None)
        )

    def __setitem__(self, question_uuid, value):  # noqa
        if not isinstance(value, SolutionState.QuestionAnswer):
            raise TypeError('You must use QuestionAnswer instance')

        question_uuid = str(question_uuid)

        self.answers[question_uuid] = dict(
            show_hint=value.show_hint,
            show_solution=value.show_solution,
            answer=value.answer
        )


class SolutionQuiz(Solution):
    # id of attempt
    attempt = models.PositiveIntegerField(default=0, null=False)

    # JSON serialized answers
    answers = JSONField()  # ZWPA: Database Session State

    @cached_property
    def state(self):
        return SolutionState(self)
