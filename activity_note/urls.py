from django.urls import path

from . import views

urlpatterns = [
    path('', views.show, name='show'),
    path('complete', views.complete, name='complete'),
    path('uncomplete', views.uncomplete, name='uncomplete'),
]
