from rest_framework import serializers
from .models import MaintenanceForm, InventoryUsage

class MaintenanceFormSerializer(serializers.ModelSerializer):
    maintenance_image = serializers.ImageField(required=False)

    class Meta:
        model = MaintenanceForm
        fields = [
            "id",
            "filed_by",
            "mmu_id",
            "odometer",
            "equipment",
            "description",
            "is_repaired",
            "status",
            "created_at",
            "resolved_at",
            "maintenance_image",
        ]
        read_only_fields = ["id", "created_at", "resolved_at"]

class InventoryUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryUsage
        fields = ["id", "reported_by", "item_name", "quantity_used", "camp_location", "date"]
        read_only_fields = ["id", "date"]
