from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # ScheduleViewSet, 
    # schedule_summary, 
    # mark_schedule_completed, 
    # schedule_for_fielduser,
    upload_mmu_excel,
    MMUAssignmentViewSet,
    update_mmu,
    service_details,
    mmu_list,
    mmu_schedules,
    camps_by_mmu,
    ScheduleViewSet,
    delete_all_assignments,
    all_assignments,
)

router = DefaultRouter()
router.register(r'assignments', MMUAssignmentViewSet, basename='assignments')
router.register(r'schedules', ScheduleViewSet, basename='schedules')


urlpatterns = [
    path("camps-by-mmu/<str:mmu_number>/", camps_by_mmu),
    path("mmu/<str:mmu_number>/", mmu_schedules),
    path("upload-mmu-excel/", upload_mmu_excel),
    path("service-details/<int:service_no>/", service_details),
    path("assignments/<int:pk>/update-mmu/", update_mmu),
    path("mmu-list/", mmu_list),
    path("assignments/delete-all/", delete_all_assignments),
    path("assignments/all/", all_assignments),
    path('', include(router.urls)),
]
