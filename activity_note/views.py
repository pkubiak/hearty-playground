from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from .models import SolutionNote
from django.views.decorators.http import require_http_methods
from django.utils import timezone


@require_http_methods(["GET", "POST"])
def Show(request, course, activity):
    if request.method == 'GET':
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
            'is_completed': is_completed,
            'completed_at': completed_at
        })

    if request.method == "POST":
        if not activity.completable:
            return HttpResponseBadRequest('Note is not completable')

        obj, _created = SolutionNote.objects.get_or_create(
            user_id=request.user.id,
            activity_id=activity.id,
        )

        completed = (request.POST['completed'] == 'true')

        obj.completed = completed
        obj.completed_at = timezone.now() if completed else None
        obj.save()

        if completed:
            redirect_url = reverse('course_app:details', args=(course.slug,))
        else:
            redirect_url = reverse('course_app:activity', args=(course.slug, str(activity.id), ''))

        return HttpResponseRedirect(redirect_url)

    return None  # NOTE: this line should be unreachable because of @require_http_methods decorator
