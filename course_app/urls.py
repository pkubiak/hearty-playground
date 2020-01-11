from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='courses.index'),
    path('<slug:slug>/', views.details, name='course.details')
]
