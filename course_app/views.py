from django.shortcuts import render


def index(request):
    return render(request, 'courses_app/index.html', {})
