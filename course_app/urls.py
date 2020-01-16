from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='courses.index'),
    path('<slug:slug>/', views.details, name='course.details'),
    re_path('^(?P<slug>[-a-zA-Z0-9_]+)/activity/(?P<activity_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/(?P<url>.*)$', views.activity, name='course.activity'),
]
