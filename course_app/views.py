from django.shortcuts import render
from .models import Course, Activity
from django.db import models
from importlib import import_module


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


def activity(request, slug, activity_uuid):
    course = Course.objects.get(slug=slug)
    activity_obj = Activity.objects.get(id=activity_uuid)


    app_name = activity_obj._meta.app_label
    views = import_module(f"{app_name}.views")
    assert hasattr(views, 'show')
    return getattr(views, 'show')(request, course, activity_obj)
