from django.shortcuts import render
from .models import Course, Activity, Solution, Lesson
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

    lessons = course.lesson_set.all()
    lessons = [
        (lesson, lesson.activity_set.all()) for lesson in lessons
    ]

    # Optimized fetchin user solutions for all activities in course
    activity_ids = [activity.id for _, activities in lessons for activity in activities]

    is_completed = Solution.objects.filter(activity_id__in=activity_ids, user_id=request.user.id).values_list('activity_id', 'completed')
    is_completed = {activity_id: completed for activity_id, completed in is_completed}

    # Add field to activities
    for _, activities in lessons:
        for activity in activities:
            activity.is_completed_by_current_user = is_completed.get(activity.id, False)

    return render(request, 'course_app/details.html', {
        'course': course,
        'lessons': lessons
    })


def activity(request, slug, activity_uuid, url):
    """Polymorphic view which pass through request to appropriete activity app."""
    course = Course.objects.get(slug=slug)
    activity_obj = Activity.objects.get(id=activity_uuid)

    app_name = activity_obj._meta.app_label

    module_name = f'{app_name}.urls'
    view, args, kwargs = resolve('/' + url, module_name)

    return view(request, *args, course=course, activity=activity_obj, **kwargs)
