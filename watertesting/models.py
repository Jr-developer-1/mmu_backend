from django.db import models

class WaterSourceTest(models.Model):
    sourceName = models.CharField(max_length=100)
    gpsLat = models.CharField(max_length=50, blank=True, null=True)
    gpsLong = models.CharField(max_length=50, blank=True, null=True)
    waterType = models.CharField(max_length=100)
    sampleDate = models.DateField()
    chlorineLevel = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[("Safe", "Safe"), ("Unsafe", "Unsafe")])
    reportFile = models.FileField(upload_to='water_reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sourceName} - {self.status}"
