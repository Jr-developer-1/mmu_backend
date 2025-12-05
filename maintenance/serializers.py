from rest_framework import serializers
from .models import FieldMaintenance

class FieldMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldMaintenance
        fields = "__all__"
