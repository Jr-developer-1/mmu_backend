from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PatientVisit
from .serializers import PatientVisitSerializer
from notifications.models import Notification
from django.db.models import Q

class PatientVisitViewSet(viewsets.ModelViewSet):
    queryset = PatientVisit.objects.all().order_by('-created_at')
    serializer_class = PatientVisitSerializer

    @action(detail=False, methods=['get'])
    def disease_summary(self, request):
        summary = (
            PatientVisit.objects
            .values('district', 'disease_category')
            .annotate(count=models.Count('id'))
        )
        return Response(summary)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        aadhaar = request.GET.get("aadhaar", "").strip()
        name = request.GET.get("name", "").strip()

        qs = PatientVisit.objects.all()

        if aadhaar:
            # Aadhaar is unique → exact match
            qs = qs.filter(aadhaar=aadhaar)
        elif len(name) >= 3:
            # optional: still allow name search if needed (web, etc.)
            qs = qs.filter(patient_name__icontains=name)
        else:
            # nothing valid sent
            return Response([])

        results = qs.order_by('-created_at')[:10]
        serializer = PatientVisitSerializer(results, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        instance = serializer.save()
        # 🔔 Generate alert when a sudden rise is detected
        category_count = PatientVisit.objects.filter(
            disease_category=instance.disease_category,
            district=instance.district
        ).count()
        if category_count % 10 == 0:  # every 10 new cases
            Notification.objects.create(
                message=f"Alert: {category_count} new {instance.get_disease_category_display()} cases in {instance.district}.",
                source="Disease Profiling System"
            )
