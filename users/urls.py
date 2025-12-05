from django.urls import path
from .api import get_users, create_user, toggle_active

urlpatterns = [
    path("", get_users),
    path("create/", create_user),
    path("toggle/<int:user_id>/", toggle_active),
]
