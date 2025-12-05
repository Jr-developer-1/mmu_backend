from django.db import models
from django.conf import settings

TEST_CHOICES = [
    ("HB", "Hemoglobin"),
    ("RBS", "Random Blood Sugar"),
    ("CBC", "Complete Blood Count"),
    ("URINE", "Urine Test"),
    ("RDT", "Rapid Diagnostic Test"),
    ("OTHER", "Other"),
]

RESULT_CHOICES = [
    ("NORMAL", "Normal"),
    ("ABNORMAL", "Abnormal"),
    ("PENDING", "Pending"),
]

class LabTest(models.Model):
    patient_name = models.CharField(max_length=200)
    patient_id = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    test_name = models.CharField(max_length=20, choices=TEST_CHOICES, default="OTHER")
    sample_date = models.DateField()
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default="PENDING")
    result_value = models.CharField(max_length=200, blank=True, null=True)  # numeric/text reading
    report_file = models.FileField(upload_to="lab_reports/", blank=True, null=True)
    mmu_id = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sample_date", "-created_at"]

    def __str__(self):
        return f"{self.patient_name} — {self.test_name} ({self.sample_date})"
