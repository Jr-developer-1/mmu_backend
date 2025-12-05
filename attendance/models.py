from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# --- Roles for each MMU staff ---
class MMU(models.Model):
    mmu_name = models.CharField(max_length=100, unique=True)
    district = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.mmu_name
    
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('FIELD', 'Field User'),
        ('OE', 'Operational Executive'),
        ('DM', 'District Manager'),
        ('RM', 'Regional Manager'),
        ('STATE', 'State Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Staff(models.Model):
    username = models.CharField(max_length=100, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="staff")
    
    def __str__(self):
        return self.username

class AttendanceRecord(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    username = models.CharField(max_length=100) 
    def __str__(self):
        return f"{self.staff.name} - {self.attendance_date}"

