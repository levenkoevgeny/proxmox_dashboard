from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static
from dashboard import views

urlpatterns = [
    path("", RedirectView.as_view(url="/pm/pm-list/")),
    path('admin/', admin.site.urls),
    path("health/", views.health_check),
    path("pm/", include("dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
