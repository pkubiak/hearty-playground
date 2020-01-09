from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pomoc/', include('help_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('user_app.urls')),
    path('', RedirectView.as_view(url='pomoc/')),
]
