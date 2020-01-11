from django.shortcuts import render
from .models import Course


def index(request):
    all_courses = list(Course.objects.all())

    highlighted = all_courses.pop()

    return render(request, 'course_app/index.html', {
        'all_courses': all_courses,
        'highlighted': highlighted
    })
