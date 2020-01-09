from django.urls import path

from . import views

urlpatterns = [
    path('', views.profile, name='user_profile'),
    # path('<slug:slug>/', views.show, name='show'),
]
