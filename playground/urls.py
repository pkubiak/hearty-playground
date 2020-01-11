from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from .views import markdown_preview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pomoc/', include('help_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('user_app.urls')),
    path('courses/', include('course_app.urls')),
    path('', RedirectView.as_view(url='pomoc/')),
    path('markdown/', markdown_preview, name='markdown_preview'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
