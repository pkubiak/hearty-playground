from django.shortcuts import render
from django.utils import translation
from django.conf import settings
import random
from django.contrib.auth.decorators import login_required
from course_app.models import Solution


@login_required
def profile(request):
    user_language = random.choice(['en', 'pl'])
    translation.activate(user_language)
    # response = HttpResponse(...)
    response = render(request, 'user_app/profile.html', {})
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)

    return response


@login_required
def statistics(request):
    solutions = Solution.objects.filter(user_id=request.user.id).order_by('-updated_at')[:8]

    in_progress_count = Solution.objects.filter(user_id=request.user.id, completed=False).count()
    completed_count = Solution.objects.filter(user_id=request.user.id, completed=True).count()

    achievements = [
        dict(icon='fab fa-html5', name='HTML5 master', color='primary'),
        dict(icon='fas fa-dragon', name='Fire dragon of CSS', color='danger'),
        dict(icon='fas fa-hat-wizard', name='Wizard of the Web', color='secondary'),
        dict(icon='fab fa-js', name='Javascript Ninja', color='warning'),
        dict(icon='fas fa-pizza-slice', name='Pizza eater', color='primary'),
        dict(icon='fas fa-hand-holding-heart', name='Hearty Playground Supporter', color='danger'),
        dict(icon='fas fa-heart', name='Hearty Foundation Member', color='danger'),
        dict(icon='far fa-keyboard', name='Fast typper', color='success'),
    ]

    return render(request, 'user_app/statistics.html', {
        'solutions': solutions,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'achievements': achievements
    })
