from django.db import models
from django.utils import timezone

class Equipment(models.Model):
    EQUIPMENT_STATUS = [
        ("Functional", "Functional"),
        ("Non-Functional", "Non-Functional"),
        ("Under Maintenance", "Under Maintenance"),
    ]

    MAINTENANCE_ALERTS = [
        ("None", "None"),
        ("Pending Maintenance", "Pending Maintenance"),
        ("Pending Calibration", "Pending Calibration"),
        ("Delayed Maintenance", "Delayed Maintenance"),
    ]

    equipment_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    gps_coordinates = models.CharField(max_length=100, blank=True, null=True)
    inspection_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=30, choices=EQUIPMENT_STATUS, default="Functional")
    maintenance_alert = models.CharField(max_length=50, choices=MAINTENANCE_ALERTS, default="None")
    inspection_image = models.ImageField(upload_to='equipment_inspections/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.equipment_name
