from django.db import models
from django.utils import timezone

class MaintenanceForm(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
    ]

    filed_by = models.CharField(max_length=150)
    equipment = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    resolved_at = models.DateTimeField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    mmu_id = models.CharField(max_length=100, null=True, blank=True)
    odometer = models.CharField(max_length=50, null=True, blank=True)
    is_repaired = models.BooleanField(default=False)
    maintenance_image = models.ImageField(
        upload_to="maintenance/",
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.mmu_id} | {self.equipment} | {self.filed_by}"


class InventoryUsage(models.Model):
    """
    When a field user uses inventory at a camp (consumable used),
    they report the item and quantity used.
    """
    reported_by = models.CharField(max_length=150)  # username
    item_name = models.CharField(max_length=200)
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2)
    camp_location = models.CharField(max_length=250, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.item_name} x{self.quantity_used} by {self.reported_by}"
