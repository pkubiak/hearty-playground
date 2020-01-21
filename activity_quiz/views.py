from django.shortcuts import render
from django.http import HttpResponse



def show(request, course, activity):
    current = int(request.POST.get('next', 0))

    total_count = activity.question_set.count()
    question = activity.question_set.all()[current]

    return render(request, 'activity_quiz/show.html', {
        'course': course,
        'activity': activity,
        'current': current,
        'total_count': total_count,
        'question': question,
        'question_type': question.__class__.__name__,
        'question_statuses': [False] * total_count,
    })
    # return HttpResponse(f"ActivityQuiz course: {course}, activity: {activity}; request: {request}")
