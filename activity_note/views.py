import markdown
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from .models import SolutionNote


def show(request, course, activity):
    content = markdown.markdown(activity.text)

    solution = SolutionNote.objects.filter(
        user_id=request.user.id,
        activity_id=activity.id,
        completed=True
    ).first()

    is_completed = solution is not None
    completed_at = solution.completed_at if solution else None

    return render(request, 'activity_note/show.html', {
        'course': course,
        'activity': activity,
        'content': content,
        'is_completed': is_completed,
        'completed_at': completed_at
    })


def complete(request, course, activity):
    obj, created = SolutionNote.objects.get_or_create(
        user_id=request.user.id,
        activity_id=activity.id,
    )

    if not created and obj.completed:
        raise ValueError('Note already completed')

    if not activity.completable:
        raise ValueError('Note is not completable')

    obj.completed = True
    obj.completed_at = datetime.now()
    obj.save()

    return HttpResponse("OK")


def uncomplete(request, course, activity):
    obj = SolutionNote.objects.get(
        user_id=request.user.id,
        activity_id=activity.id,
        completed=True
    )

    if not activity.completable:
        raise ValueError('Note is not completable')

    obj.completed = False
    obj.completed_at = None
    obj.save()

    return HttpResponse("OK")
