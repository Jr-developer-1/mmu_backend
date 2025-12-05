from rest_framework import serializers
from .models import LabTest

class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = "__all__"
        read_only_fields = ("id", "created_at", "created_by")
