from django.db import models
from django.conf import settings

class PVTGCamp(models.Model):
    camp_name = models.CharField(max_length=255)
    date = models.DateField()
    state = models.CharField(max_length=128, blank=True)
    district = models.CharField(max_length=128, blank=True)
    mandal = models.CharField(max_length=128, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    population_served = models.PositiveIntegerField(default=0)
    services_provided = models.CharField(max_length=512, blank=True)  # comma separated tags
    attendees_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.camp_name} ({self.date})"
