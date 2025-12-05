from rest_framework import serializers
from .models import WaterSourceTest

class WaterSourceTestSerializer(serializers.ModelSerializer):
    reportFile = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = WaterSourceTest
        fields = [
            "id",
            "sourceName",
            "gpsLat",
            "gpsLong",
            "waterType",
            "sampleDate",
            "chlorineLevel",
            "status",
            "reportFile",
        ]
