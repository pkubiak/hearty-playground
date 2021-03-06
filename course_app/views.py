from django.shortcuts import render
from .models import Course, Activity, Solution
from django.urls import resolve
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """Display list of all available courses."""
    all_courses = list(Course.objects.all())

    highlighted = all_courses.pop()

    return render(request, 'course_app/index.html', {
        'all_courses': all_courses,
        'highlighted': highlighted
    })


@login_required
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

    # Compute current user completion score
    for lesson, activities in lessons:
        lesson.current_user_score = sum(activity.score for activity in activities if activity.is_completed_by_current_user)
        total_score = lesson.total_score
        if total_score:
            lesson.current_user_progress = 100.0 * lesson.current_user_score / total_score

    return render(request, 'course_app/details.html', {
        'course': course,
        'lessons': lessons
    })


@login_required
def activity(request, slug, activity_uuid, url):
    """Polymorphic view which pass through request to appropriete activity app."""
    course = Course.objects.get(slug=slug)
    activity_obj = Activity.objects.get(id=activity_uuid)

    app_name = activity_obj._meta.app_label

    module_name = f'{app_name}.urls'
    view, args, kwargs = resolve('/' + url, module_name)

    return view(request, *args, course=course, activity=activity_obj, **kwargs)
