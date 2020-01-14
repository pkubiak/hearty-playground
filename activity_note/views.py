import markdown
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def show(request, course, activity):
    # return HttpResponse(f"ActivityNote course: {course}, activity: {activity}; request: {request}")
    content = markdown.markdown(activity.text)
    return render(request, 'activity_note/show.html', {
        'course': course,
        'activity': activity,
        'content': content
    })
