from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import MaintenanceForm, InventoryUsage
from .serializers import MaintenanceFormSerializer, InventoryUsageSerializer


# ------------------- CAMPS FOR USER -------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def fielduser_camps(request, username):
    try:
        from schedule.models import Schedule
    except:
        return Response([], status=200)

    qs = Schedule.objects.filter(assigned_to__username=username).values(
        "id", "date", "location", "route_code", "compliance", "distance"
    )
    return Response(list(qs), status=200)


# ------------------- MAINTENANCE HISTORY -------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def maintenance_for_user(request, username):
    qs = MaintenanceForm.objects.filter(
        filed_by__iexact=username
    ).order_by("-created_at")

    serializer = MaintenanceFormSerializer(qs, many=True)
    return Response(serializer.data)


# ------------------- SUBMIT MAINTENANCE (WITH IMAGE UPLOAD) -------------------
@api_view(["POST"])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def submit_maintenance(request):
    data = request.data.copy()

    # Convert filed_by ID → username
    filed_by = data.get("filed_by")
    if filed_by is None:
        return Response({"error": "filed_by is required"}, status=400)

    if str(filed_by).isdigit():
        try:
            from users.models import User
            user_obj = User.objects.get(id=int(filed_by))
            data["filed_by"] = user_obj.username
        except:
            pass

    # Convert Yes/No → Boolean
    repaired = data.get("is_repaired")
    if repaired is not None:
        data["is_repaired"] = True if str(repaired).lower() in ["yes", "true", "1"] else False

    # ⭐ DO NOT pass "files=" argument
    serializer = MaintenanceFormSerializer(data=data)

    if serializer.is_valid():
        serializer.save()   # ⭐ This will save uploaded image
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

# ------------------- INVENTORY USE -------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def inventory_use(request):
    data = request.data.copy()
    required = ["reported_by", "item_name", "quantity_used"]

    for r in required:
        if r not in data:
            return Response({"error": f"{r} is required"}, status=400)

    serializer = InventoryUsageSerializer(data=data)

    if serializer.is_valid():
        instance = serializer.save()

        # Optional: reduce stock in inventory app
        try:
            from inventory.models import Inventory as InventoryItem
            inv = InventoryItem.objects.filter(
                item_name__iexact=instance.item_name
            ).first()

            if inv:
                inv.quantity = float(inv.quantity) - float(instance.quantity_used)
                inv.save()

        except:
            pass

        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


# ------------------- UPDATE MAINTENANCE -------------------
@api_view(["PATCH"])
@permission_classes([AllowAny])
def update_maintenance(request, id):
    try:
        obj = MaintenanceForm.objects.get(id=id)
    except MaintenanceForm.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    serializer = MaintenanceFormSerializer(obj, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)


# ------------------- DELETE MAINTENANCE -------------------
@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_maintenance(request, id):
    try:
        obj = MaintenanceForm.objects.get(id=id)
    except MaintenanceForm.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    obj.delete()
    return Response({"message": "Deleted"}, status=200)


# ------------------- ALERT LIST -------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def maintenance_alerts(request):
    qs = MaintenanceForm.objects.filter(
        is_repaired=False,
        is_resolved=False
    ).order_by("-created_at")

    alerts = [
        {
            "id": i.id,
            "mmu_id": i.mmu_id or "",
            "equipment": i.equipment or "",
            "description": i.description or "",
            "created_at": i.created_at.strftime("%Y-%m-%d"),
        }
        for i in qs
    ]

    return Response(alerts)


# ------------------- RESOLVE ALERT -------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def resolve_alert(request, id):
    try:
        m = MaintenanceForm.objects.get(id=id)
    except MaintenanceForm.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    m.is_resolved = True
    m.save()

    return Response({"success": True})
