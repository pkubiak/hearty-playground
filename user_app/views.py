from django.shortcuts import render
from django.utils import translation
from django.conf import settings
import random


def profile(request):
    user_language = random.choice(['en', 'pl'])
    translation.activate(user_language)
    # response = HttpResponse(...)
    response = render(request, 'user_app/profile.html', {})
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)

    return response
