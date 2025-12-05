# mmu_backend/vehicle/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, ELogViewSet, InspectionViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicles')
# for frontend convenience we expose logs and inspections under the /vehicle/ base path
router.register(r'elog', ELogViewSet, basename='elog')
router.register(r'inspections', InspectionViewSet, basename='inspections')

urlpatterns = [
    path('', include(router.urls)),
]
