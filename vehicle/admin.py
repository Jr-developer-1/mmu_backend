# mmu_backend/vehicle/admin.py
from django.contrib import admin
from .models import Vehicle, ELog, VehicleInspection

admin.site.register(Vehicle)
admin.site.register(ELog)
admin.site.register(VehicleInspection)
