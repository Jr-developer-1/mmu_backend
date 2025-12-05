from django.urls import path
from . import views

urlpatterns = [
    path("schedule/fielduser/<str:username>/", views.fielduser_camps, name="field-camps"),
    path("maintenance/fielduser/<str:username>/", views.maintenance_for_user, name="field-maintenance"),
    path("maintenance/submit/", views.submit_maintenance, name="submit-maintenance"),
    path("inventory/use/", views.inventory_use, name="inventory-use"),
    path("maintenance/alerts/", views.maintenance_alerts),
    path("maintenance/alerts/resolve/<int:id>/", views.resolve_alert),
    path("update/<int:id>/", views.update_maintenance),
    path("delete/<int:id>/", views.delete_maintenance),
]
