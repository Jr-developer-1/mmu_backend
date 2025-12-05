from django.db import models
from django.utils import timezone

class Notification(models.Model):
    message = models.CharField(max_length=255)
    source = models.CharField(max_length=100, default="System")
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.source} - {self.message}"
