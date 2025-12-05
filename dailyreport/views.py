from rest_framework import viewsets, permissions
from .models import DailyServiceReport
from .serializers import DailyServiceReportSerializer

class DailyServiceReportViewSet(viewsets.ModelViewSet):
    queryset = DailyServiceReport.objects.all().order_by('-date')
    serializer_class = DailyServiceReportSerializer
    permission_classes = [permissions.AllowAny]
