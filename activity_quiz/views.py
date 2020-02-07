from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def show(request, course, activity):
    return HttpResponse(f"ActivityQuiz course: {course}, activity: {activity}; request: {request}")
