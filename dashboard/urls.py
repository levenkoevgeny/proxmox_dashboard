from django.urls import path

from . import views

urlpatterns = [
    path("pm-list/", views.pm_list, name="pm_list"),
]