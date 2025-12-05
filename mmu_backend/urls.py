from django.contrib import admin
from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static
from field import views

urlpatterns = [
    path("api/", include("authapi.urls")),
    path('admin/', admin.site.urls),
    path('api/', include('attendance.urls')),
    path('api/schedule/', include('schedule.urls')),
    path('api/', include('inventory.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('opdata.urls')),
    path('api/', include('watertesting.urls')),
    path('api/', include('equipment.urls')),
    path('api/', include('dailyreport.urls')),
    path('api/vehicle/', include('vehicle.urls')),
    path('api/pvtg/', include('pvtg.urls')),
    path("api/lab/", include("lab.urls")),
    path('api/users/', include('users.urls')),
    path('api/manage-users/', include('users.urls')),
    path('api/manage-users/create/', include('users.urls')),
    # path("api/field/maintenance/", include("maintenance.urls")),
    path("api/field/", include("field.urls")),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-auth/', include('rest_framework.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)