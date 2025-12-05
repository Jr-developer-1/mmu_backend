# mmu_backend/vehicle/models.py
from django.db import models
from django.conf import settings

class Vehicle(models.Model):
    registration = models.CharField(max_length=64, unique=True)
    model = models.CharField(max_length=128, blank=True)
    driver_name = models.CharField(max_length=128, blank=True)
    current_odometer = models.PositiveIntegerField(null=True, blank=True)
    on_road = models.BooleanField(default=False)
    fitness_due = models.DateField(null=True, blank=True)  # alert if due

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.registration} - {self.model}"

class ELog(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name="logs", on_delete=models.CASCADE)
    odometer = models.PositiveIntegerField()
    fuel_ltr = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    note = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"log {self.vehicle.registration} @ {self.odometer}"

class VehicleInspection(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name="inspections", on_delete=models.CASCADE)
    inspection_date = models.DateField()
    checklist_ok = models.BooleanField(default=True)
    issues = models.TextField(blank=True)
    inspector = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"inspect {self.vehicle.registration} on {self.inspection_date}"
