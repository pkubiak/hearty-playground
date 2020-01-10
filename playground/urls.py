from django.contrib import admin
from django.urls import include, path
from .views import markdown_preview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pomoc/', include('help_app.urls')),
    path('markdown/', markdown_preview, name='markdown_preview'),
]
