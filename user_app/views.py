from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from course_app.models import Solution
from .models import Achievement
from django.db.models import F


@login_required
def profile(request):
    # user_language = random.choice(['en', 'pl'])
    # translation.activate(user_language)
    # response = HttpResponse(...)
    response = render(request, 'user_app/profile.html', {})
    # response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)

    return response


@login_required
def statistics(request):
    solutions = Solution.objects.filter(user_id=request.user.id).order_by('-updated_at')[:8]

    in_progress_count = Solution.objects.filter(user_id=request.user.id, completed=False).count()
    completed_count = Solution.objects.filter(user_id=request.user.id, completed=True).count()

    achievements = Achievement.objects.filter(user__id=request.user.id).annotate(acquired_at=F('acquiredachievement__acquired_at')).\
        order_by('acquired_at').all()

    return render(request, 'user_app/statistics.html', {
        'solutions': solutions,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'achievements': achievements
    })
