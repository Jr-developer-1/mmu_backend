from rest_framework import viewsets, permissions, status,filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from datetime import date
from django.db import models
from .models import AttendanceRecord, Staff, Role
from .serializers import StaffSerializer, AttendanceRecordSerializer, RoleSerializer


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "ADMIN"
    
# class StaffViewSet(viewsets.ModelViewSet):
#     queryset = Staff.objects.all()
#     serializer_class = StaffSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['username', 'name']

# 🔹 Role ViewSet (for Add Role page)
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('id')
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]  

    def perform_create(self, serializer):
        serializer.save()


# 🔹 Staff ViewSet (for employee management)
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]


# 🔹 Attendance management
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [AllowAny]


# 🔹 Summary API for dashboard counts
@api_view(['GET'])
@permission_classes([AllowAny])
def attendance_summary(request):
    today = date.today()
    today_records = AttendanceRecord.objects.filter(attendance_date=today)
    total_present = today_records.count()

    role_counts = today_records.values('staff__role__name').annotate(count=models.Count('id'))
    role_data = {role['staff__role__name']: role['count'] for role in role_counts}

    return Response({
        "total_present": total_present,
        "roles": role_data
    })


# 🔹 Current logged-in user info
User = get_user_model()

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": getattr(user, "email", ""),
        "role": getattr(user, "role", None),
    })
    
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([AllowAny])
def manage_roles(request, pk=None):
    if request.method == 'GET':
        roles = Role.objects.all().order_by('id')
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not pk:
            return Response({'error': 'Role ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            role = Role.objects.get(pk=pk)
            role.delete()
            return Response({'message': 'Role deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Role.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
