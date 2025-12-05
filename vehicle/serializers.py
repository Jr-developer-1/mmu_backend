# mmu_backend/vehicle/serializers.py
from rest_framework import serializers
from .models import Vehicle, ELog, VehicleInspection

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class ELogSerializer(serializers.ModelSerializer):
    vehicle_registration = serializers.CharField(source='vehicle.registration', read_only=True)
    class Meta:
        model = ELog
        fields = ['id','vehicle','vehicle_registration','odometer','fuel_ltr','note','created_by','created_at']
        read_only_fields = ['created_by','created_at']

class VehicleInspectionSerializer(serializers.ModelSerializer):
    vehicle_registration = serializers.CharField(source='vehicle.registration', read_only=True)
    class Meta:
        model = VehicleInspection
        fields = ['id','vehicle','vehicle_registration','inspection_date','checklist_ok','issues','inspector','created_at']
        read_only_fields = ['inspector','created_at']
