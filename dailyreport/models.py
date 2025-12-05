from django.db import models

class DailyServiceReport(models.Model):
    date = models.DateField(auto_now_add=True)
    mmu_name = models.CharField(max_length=100)
    village_name = models.CharField(max_length=100)
    session_type = models.CharField(
        max_length=50,
        choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon')],
        default='Morning'
    )
    total_patients = models.PositiveIntegerField(default=0)
    elderly = models.PositiveIntegerField(default=0)
    pregnant_women = models.PositiveIntegerField(default=0)
    infants = models.PositiveIntegerField(default=0)
    chronic_cases = models.PositiveIntegerField(default=0)
    palliative_cases = models.PositiveIntegerField(default=0)

    anm_participation = models.BooleanField(default=False)
    aww_participation = models.BooleanField(default=False)
    asha_participation = models.BooleanField(default=False)
    feedback_received = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mmu_name} - {self.village_name} ({self.session_type})"
