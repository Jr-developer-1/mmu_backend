# MMU-WEBAPP/mmu_backend/attendance/tasks.py
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import MMUVehicle, MMUStaff, AttendanceRecord
from datetime import date

@shared_task
def generate_daily_attendance_and_alerts(target_date=None):
    """
    generate summary for all MMUs for target_date (default today),
    and send alert emails for deviations (absentees > 0).
    """
    if not target_date:
        target_date = date.today().isoformat()

    alerts = []
    for mmu in MMUVehicle.objects.all():
        assigned = MMUStaff.objects.filter(mmu=mmu, active=True)
        total_assigned = assigned.count()
        present_user_ids = AttendanceRecord.objects.filter(mmu=mmu, attendance_date=target_date).values_list('user_id', flat=True)
        absentees = assigned.exclude(user_id__in=present_user_ids)
        if absentees.exists():
            # build alert
            alert_text = f"MMU {mmu.mmu_code} has {absentees.count()} absentees on {target_date}"
            alerts.append(mmu, alert_text, list(absentees.values('user__username','role')))

            # send email to OE/DM - placeholder: you must map who OE/DM emails are
            # Here we use a generic setting ADMIN_EMAILS (ensure in settings)
            recipients = getattr(settings, "ATTENDANCE_ALERT_EMAILS", [])
            subject = f"Attendance Deviation: {mmu.mmu_code} ({target_date})"
            message = f"{alert_text}\n\nAbsentees:\n"
            for a in absentees:
                message += f"- {a.user.username} ({a.role})\n"
            if recipients:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=True)

    return {"date": target_date, "alerts_sent": len(alerts)}
