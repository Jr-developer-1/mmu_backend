from django.db import models

class FieldMaintenance(models.Model):
    filed_by = models.CharField(max_length=100)
    mmu_id = models.CharField(max_length=50)
    odometer = models.IntegerField()
    equipment = models.CharField(max_length=100)
    description = models.TextField()
    repaired = models.CharField(max_length=10, default="No")

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="PENDING")
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.filed_by} - {self.equipment}"
