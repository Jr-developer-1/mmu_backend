from django.contrib import admin
from .models import Staff, AttendanceRecord

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role')  
    search_fields = ('name', 'role')

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('username', 'attendance_date', 'time_in', 'time_out', 'staff')
    search_fields = ('username', 'staff__name')