# mmu_backend/vehicle/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vehicle, ELog, VehicleInspection
from .serializers import VehicleSerializer, ELogSerializer, VehicleInspectionSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by('-id')
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def set_status(self, request, pk=None):
        v = get_object_or_404(Vehicle, pk=pk)
        on_road = request.data.get('on_road', None)
        if on_road is None:
            return Response({'error':'on_road required'}, status=status.HTTP_400_BAD_REQUEST)
        v.on_road = bool(on_road)
        v.save()
        return Response({'id': v.id, 'on_road': v.on_road})

class ELogViewSet(viewsets.ModelViewSet):
    queryset = ELog.objects.all().order_by('-created_at')
    serializer_class = ELogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # update vehicle odometer if provided
        instance = serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)
        try:
            v = instance.vehicle
            if instance.odometer:
                v.current_odometer = instance.odometer
                v.save()
        except Exception:
            pass

class InspectionViewSet(viewsets.ModelViewSet):
    queryset = VehicleInspection.objects.all().order_by('-inspection_date')
    serializer_class = VehicleInspectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(inspector=self.request.user if self.request.user.is_authenticated else None)
