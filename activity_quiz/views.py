from django.shortcuts import render
from .models import SolutionQuiz, Question, SingleChoiceQuestion, MultipleChoiceQuestion, OpenQuestion


def show_summary(request, course, activity, solution):
    return render(request, 'activity_quiz/submit.html', {
        'course': course,
        'activity': activity,
    })


def show(request, course, activity):
    solution, created = SolutionQuiz.objects.get_or_create(
        user_id=request.user.id,
        activity_id=activity.id,
        defaults={'answers': {}}
    )

    current = int(request.POST.get('next', 0))

    if current == -1:
        return show_summary(request, course, activity, solution)

    questions_ids = list(map(str, activity.question_set.all().values_list('id', flat=True)))
    total_count = len(questions_ids)

    if request.method == 'POST':
        print('*' * 100)
        print(request.POST)
        print('*' * 100)

        if 'current' in request.POST:
            obj = Question.objects.get(id=request.POST['current'], activity_id=activity.id)
            if isinstance(obj, SingleChoiceQuestion):
                answers = set(map(str, obj.answers_set.all().values_list('id', flat=True)))
                answer = request.POST['answer']
                if answer in answers or answer is None:
                    solution.answers[str(obj.id)] = answer
            elif isinstance(obj, MultipleChoiceQuestion):
                answers = set(map(str, obj.answers_set.all().values_list('id', flat=True)))
                answer = set(request.POST.getlist('answer'))
                answer &= answers
                solution.answers[str(obj.id)] = list(answer)
            elif isinstance(obj, OpenQuestion):
                solution.answers[str(obj.id)] = str(request.POST.get('answer'))

    solution.save()

    question = activity.question_set.all()[current]

    return render(request, question.template, {
        'course': course,
        'activity': activity,
        'current': current,
        'total_count': total_count,
        'question': question,
        'question_type': question.__class__.__name__,
        'statuses': [bool(solution.answers.get(key)) for key in questions_ids],
        'solution': solution.answers.get(str(question.id), None)
    })
