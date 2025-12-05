from rest_framework import routers
from .views import WaterSourceTestViewSet

router = routers.DefaultRouter()
router.register(r'watertesting', WaterSourceTestViewSet)

urlpatterns = router.urls
