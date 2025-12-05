from django.db import models
from django.utils import timezone

class PatientVisit(models.Model):
    patient_name = models.CharField(max_length=100)

    # Newly added fields
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    aadhaar = models.CharField(max_length=12, blank=True, null=True)

    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    
    district = models.CharField(max_length=100)
    mandal = models.CharField(max_length=100)
    village = models.CharField(max_length=100)

    # New fields
    disease_name = models.CharField(max_length=200, blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    medicines = models.JSONField(default=list, blank=True, null=True)

    diagnosis = models.CharField(max_length=200)
    
    disease_category = models.CharField(
        max_length=50,
        choices=[
            ('CD', 'Communicable Disease'),
            ('NCD', 'Non-Communicable Disease'),
            ('RCH', 'Reproductive and Child Health'),
            ('MA', 'Minor Ailment/Other'),
        ],
    )

    treatment_given = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient_name} - {self.diagnosis}"
