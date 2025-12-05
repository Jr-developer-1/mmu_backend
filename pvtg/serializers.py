from rest_framework import serializers
from .models import PVTGCamp

class PVTGCampSerializer(serializers.ModelSerializer):
    class Meta:
        model = PVTGCamp
        fields = "__all__"
        read_only_fields = ("created_by","created_at")
