from django.shortcuts import render, redirect
from .models import SolutionQuiz
from datetime import datetime


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
            total_score += question.evaluate_answer(solution.state[question.id].answer)
        solution.score = total_score / total_count

        solution.save()

    completed = solution.completed

    if completed and request.POST.get('finish') == 'retake':
        solution.delete()
        return redirect('course_app:activity', course.slug, str(activity.id), '')

    # Update last question
    if request.method == 'POST' and not completed and request.POST.get('current'):
        current = int(request.POST.get('current', 0))

        question = activity.question_set.order_by('order', 'id').all()[current]

        # update stored answers
        s = solution.state[question.id]
        s.answer = question.serialize_answer(request)
        solution.state[question.id] = s

        solution.save()

    current = int(request.POST.get('next', total_count if completed else 0))

    if current == total_count:
        return render(request, 'activity_quiz/submit.html', {
            'course': course,
            'activity': activity,
            'current': current,
            'total_count': total_count,
            'statuses': [bool(solution.state[key].answer) for key in questions_ids],
            'completed': completed,
            'score': 100.0 * (solution.score or 0),
        })

    question = activity.question_set.order_by('order', 'id').all()[current]
    answer = solution.state[str(question.id)].answer

    return render(request, question.template, {
        'course': course,
        'activity': activity,
        'current': current,
        'total_count': total_count,
        'question': question,
        'statuses': [bool(solution.state[key].answer) for key in questions_ids],
        'solution': answer,
        'completed': completed,
        'score': question.evaluate_answer(answer) if completed else None
    })
