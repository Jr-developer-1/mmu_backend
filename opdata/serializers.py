from rest_framework import serializers
from .models import PatientVisit

class PatientVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientVisit
        fields = '__all__'

    def validate_phone(self, value):
        if value and len(value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits")
        return value

    def validate_aadhaar(self, value):
        if value and len(value) != 12:
            raise serializers.ValidationError("Aadhaar must be exactly 12 digits")
        return value
