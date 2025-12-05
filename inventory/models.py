from django.db import models
from django.utils import timezone

class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default="Available")
    restocked_status = models.CharField(
        max_length=20,
        default="Pending"  # Default until admin approves
    )

    def __str__(self):
        return self.item_name
