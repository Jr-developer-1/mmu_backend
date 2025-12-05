from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LabTestViewSet

router = DefaultRouter()
router.register(r"tests", LabTestViewSet, basename="labtest")

urlpatterns = [
    path("", include(router.urls)),
]
