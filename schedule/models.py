from django.db import models

class MMUAssignment(models.Model):
    service_no = models.IntegerField(unique=True)  # 1 to 904
    mmu_number = models.CharField(max_length=50)
    district = models.CharField(max_length=100)
    mandal = models.CharField(max_length=100)
    base_location = models.CharField(max_length=200)

    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)

    phc_name = models.CharField(max_length=200, blank=True, null=True)
    vhc_name = models.CharField(max_length=200, blank=True, null=True)
    vhc_code = models.CharField(max_length=100, blank=True, null=True)
    habitation = models.CharField(max_length=200, blank=True, null=True)

    lat2 = models.CharField(max_length=100, blank=True, null=True)
    long2 = models.CharField(max_length=100, blank=True, null=True)

    fixed_day = models.CharField(max_length=50, blank=True, null=True)
    week = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.service_no} - {self.mmu_number}"

class Schedule(models.Model):
    mmu_id = models.CharField(max_length=100)
    service_no = models.IntegerField(default=0)  # ADD THIS FIELD
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    state = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    mandal = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    route_code = models.CharField(max_length=50, blank=True)
    distance = models.CharField(max_length=50, blank=True)
    assigned_to = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, default="Pending")    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["mmu_id", "date"],
                name="unique_mmu_per_day"
            )
        ]
