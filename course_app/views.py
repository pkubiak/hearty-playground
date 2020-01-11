from django.shortcuts import render
from .models import Course


def index(request):
    """Display list of all available courses."""
    all_courses = list(Course.objects.all())

    highlighted = all_courses.pop()

    return render(request, 'course_app/index.html', {
        'all_courses': all_courses,
        'highlighted': highlighted
    })


def details(request, slug):
    """Display details of single course: progress and all available content."""
    course = Course.objects.get(slug=slug)

    return render(request, 'course_app/details.html', {
        'course': course
    })
