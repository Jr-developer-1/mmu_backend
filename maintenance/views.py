from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FieldMaintenance
from .serializers import FieldMaintenanceSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@api_view(["POST"])
def submit_maintenance(request):
    serializer = FieldMaintenanceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Submitted", "data": serializer.data})
    return Response(serializer.errors, status=400)

@api_view(["GET"])
def maintenance_history(request, username):
    records = FieldMaintenance.objects.filter(filed_by=username).order_by("-created_at")
    serializer = FieldMaintenanceSerializer(records, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(["PATCH"])
def update_maintenance(request, id):
    try:
        record = FieldMaintenance.objects.get(id=id)
    except FieldMaintenance.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)

    data = request.data  # DRF automatically parses JSON

    record.mmu_id = data.get("mmu_id", record.mmu_id)
    record.odometer = data.get("odometer", record.odometer)
    record.equipment = data.get("equipment", record.equipment)
    record.description = data.get("description", record.description)
    record.is_repaired = data.get("is_repaired", record.is_repaired)

    record.save()

    return JsonResponse({"success": True, "message": "Updated"})

@csrf_exempt
def delete_maintenance(request, id):
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE required"}, status=400)

    try:
        record = FieldMaintenance.objects.get(id=id)
    except FieldMaintenance.DoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)

    record.delete()

    return JsonResponse({"success": True, "message": "Deleted"})
