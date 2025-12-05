from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PVTGCampViewSet, pvtg_summary

router = DefaultRouter()
router.register(r'camps', PVTGCampViewSet, basename='camps')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', pvtg_summary, name='pvtg-summary'),
]
