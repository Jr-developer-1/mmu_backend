from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Inventory
from .serializers import InventorySerializer
from notifications.models import Notification


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all().order_by('-id')
    serializer_class = InventorySerializer
    permission_classes = [permissions.AllowAny]

    # ✅ Create notification when a new item is added
    def perform_create(self, serializer):
        instance = serializer.save()
        Notification.objects.create(
            message=f"New inventory item added: {instance.item_name}",
            source="Inventory Management"
        )

        # Optional: if item is low stock / expired
        if hasattr(instance, 'status'):
            status = str(instance.status).lower()
            if status in ["low stock", "expired", "out of stock"]:
                Notification.objects.create(
                    message=f"Inventory Alert: {instance.item_name} - {instance.status}",
                    source="Inventory Management"
                )

    # ✅ Update notification when inventory is updated
    def perform_create(self, serializer):
        instance = serializer.save()
        status = str(instance.status).lower()

        # LOW STOCK / EXPIRED / OUT OF STOCK
        if status in ["low stock", "expired", "out of stock"]:
            # ❗ Check if an active notification already exists for same item
            exists = Notification.objects.filter(
                message__icontains=instance.item_name,
                is_read=False   # unread = pending alert
            ).exists()

            if not exists:
                Notification.objects.create(
                    message=f"Inventory Alert: {instance.item_name} - {instance.status}",
                    source="Inventory Management"
                )



    # ✅ When admin clicks ✔ (acknowledge), mark item Restocked
    @action(detail=True, methods=['post'])
    def mark_restocked(self, request, pk=None):
        try:
            item = Inventory.objects.get(pk=pk)
            item.restocked_status = "Restocked"
            item.status = "Available"  # clear alert
            item.save()

            # close only related alerts
            Notification.objects.filter(
                message__icontains=item.item_name,
                is_read=False
            ).update(is_read=True)

            return Response({
                "message": f"{item.item_name} marked as Restocked and alerts cleared"
            })

        except Inventory.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)


