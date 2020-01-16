from django.shortcuts import render
from .models import Course, Activity
from django.db import models
from importlib import import_module
from django.urls import include, path
from django.urls import resolve, get_urlconf
from urllib.parse import urlparse

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


def activity(request, slug, activity_uuid, url):
    """Polymorphic view which pass through request to appropriete activity app."""
    course = Course.objects.get(slug=slug)
    activity_obj = Activity.objects.get(id=activity_uuid)

    app_name = activity_obj._meta.app_label

    module_name = f'{app_name}.urls'
    view, args, kwargs = resolve('/' + url, module_name)

    return view(request, *args, course=course, activity=activity_obj, **kwargs)
