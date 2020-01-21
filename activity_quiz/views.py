from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def show(request, course, activity):
    question = activity.question_set.first()

    return render(request, 'activity_quiz/show.html', {
        'course': course,
        'activity': activity,
        'current': 0,
        'total_questions_count': 5,
        'question': question,
        'question_statuses': [False, True, True, False, False, True],
    })
    # return HttpResponse(f"ActivityQuiz course: {course}, activity: {activity}; request: {request}")
