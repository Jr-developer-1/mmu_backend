from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from .models import PVTGCamp
from .serializers import PVTGCampSerializer
from django.db.models import Sum, Count
from datetime import date

class PVTGCampViewSet(viewsets.ModelViewSet):
    queryset = PVTGCamp.objects.all().order_by("-date","-id")
    serializer_class = PVTGCampSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(created_by=user)

# simple summary endpoint (also exposed as view)
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def pvtg_summary(request):
    total_camps = PVTGCamp.objects.count()
    total_pop = PVTGCamp.objects.aggregate(total=Sum('population_served'))['total'] or 0
    # coverage: arbitrary formula: camps covering >=100 population count
    camps_with_population = PVTGCamp.objects.filter(population_served__gt=0).count()
    coverage_percent = round((camps_with_population / (total_camps or 1)) * 100) if total_camps else 0
    return Response({
        "totalCamps": total_camps,
        "totalPopulation": total_pop,
        "coveragePercent": coverage_percent
    })
