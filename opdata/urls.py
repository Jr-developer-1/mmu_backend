from rest_framework.routers import DefaultRouter
from .views import PatientVisitViewSet

router = DefaultRouter()
router.register(r'opdata', PatientVisitViewSet, basename='opdata')

urlpatterns = router.urls
