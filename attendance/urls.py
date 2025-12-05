from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StaffViewSet, AttendanceViewSet, attendance_summary,current_user, RoleViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'staff', StaffViewSet, basename='staff')  
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'roles', RoleViewSet, basename='roles')

urlpatterns = [
    path('', include(router.urls)),
    path('attendance-summary/', attendance_summary, name='attendance-summary'),
    path('me/', current_user, name='current-user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('roles/', views.manage_roles, name='manage_roles'),
    # path('roles/<int:pk>/', views.manage_roles, name='delete_role'), 
]

