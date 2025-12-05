from rest_framework.routers import DefaultRouter
from .views import DailyServiceReportViewSet

router = DefaultRouter()
router.register(r'dailyreport', DailyServiceReportViewSet, basename='dailyreport')

urlpatterns = router.urls
