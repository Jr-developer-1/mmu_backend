from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from .models import WaterSourceTest
from .serializers import WaterSourceTestSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class WaterSourceTestViewSet(viewsets.ModelViewSet):
    queryset = WaterSourceTest.objects.all().order_by('-sampleDate')
    serializer_class = WaterSourceTestSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser) 