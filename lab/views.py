from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LabTest
from .serializers import LabTestSerializer

class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all().order_by('-sample_date', '-created_at')
    serializer_class = LabTestSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # optional: mark test result quickly
    @action(detail=True, methods=['post'])
    def mark_result(self, request, pk=None):
        test = self.get_object()
        result = request.data.get("result")
        result_value = request.data.get("result_value", "")
        if result not in dict(LabTest._meta.get_field("result").choices):
            return Response({"error": "invalid result"}, status=status.HTTP_400_BAD_REQUEST)
        test.result = result
        test.result_value = result_value
        test.save()
        return Response({"message": "updated"})
