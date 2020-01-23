from django.shortcuts import render
from .models import SolutionQuiz, Question, SingleChoiceQuestion, MultipleChoiceQuestion, OpenQuestion
from datetime import datetime


# def show_summary(request, course, activity, solution):
#     pass
#
# def show_results(request, course, activity, solution):
#     pass


def show(request, course, activity):
    solution, created = SolutionQuiz.objects.get_or_create(
        user_id=request.user.id,
        activity_id=activity.id,
        defaults={'answers': {}}
    )

    questions_ids = list(map(str, activity.question_set.all().values_list('id', flat=True)))
    total_count = len(questions_ids)

    # Finish quiz and compute final score
    if request.POST.get('finish') == 'sure' and not solution.completed:
        solution.completed = True
        solution.completed_at = datetime.now()

        total_score = 0
        for question in activity.question_set.all():
            total_score += question.evaluate_answer(solution[question.id].answer)
        solution.score = total_score / total_count

        solution.save()

    completed = solution.completed

    # Update last question
    if request.method == 'POST' and not completed:
        current = int(request.POST.get('current', 0))
        print('current:', current)

        question = activity.question_set.all()[current]

        print('*' * 100)
        print(request.POST)
        print('*' * 100)

        # update stored answers
        s = solution[question.id]
        s.answer = question.serialize_answer(request)
        solution[question.id] = s

        solution.save()

    current = int(request.POST.get('next', -1 if completed else 0))

    if current == -1:
        return render(request, 'activity_quiz/submit.html', {
            'course': course,
            'activity': activity,
            'current': current,
            'total_count': total_count,
            'statuses': [bool(solution[key].answer) for key in questions_ids],
            'completed': completed,
            'score': 100.0 * (solution.score or 0),
        })

    question = activity.question_set.all()[current]
    return render(request, question.template, {
        'course': course,
        'activity': activity,
        'current': current,
        'total_count': total_count,
        'question': question,
        'statuses': [bool(solution[key].answer) for key in questions_ids],
        'solution': solution[str(question.id)].answer,
        'completed': completed, #activity.completed,
    })
