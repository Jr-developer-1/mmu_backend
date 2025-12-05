# schedule/serializers.py
from rest_framework import serializers
from .models import MMUAssignment, Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class MMUAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MMUAssignment
        fields = [
            "id",
            "service_no",
            "mmu_number",
            "district",
            "mandal",
            "base_location",

            "latitude",
            "longitude",

            "phc_name",
            "vhc_name",
            "vhc_code",
            "habitation",

            "lat2",
            "long2",

            "fixed_day",
            "week",
        ]