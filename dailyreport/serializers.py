from rest_framework import serializers
from .models import DailyServiceReport

class DailyServiceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyServiceReport
        fields = '__all__'
