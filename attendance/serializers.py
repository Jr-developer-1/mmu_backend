from rest_framework import serializers
from .models import AttendanceRecord, Staff, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    # Display role name directly
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = Staff
        fields = [
            'id',
            'username',
            'role',
            'role_name',
        ]

class AttendanceRecordSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.name', read_only=True)
    staff_role = serializers.CharField(source='staff.role.name', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = [
            'id',
            'staff',
            'staff_name',
            'staff_role',
            'attendance_date',
            'time_in',
            'time_out',
            'username'
        ]
