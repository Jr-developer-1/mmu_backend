# maintenance/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path("submit/", views.submit_maintenance),
    path("history/<str:username>/", views.maintenance_history),
]
