from rest_framework import viewsets, status
from .models import Equipment
from rest_framework.response import Response
from django.core.files.base import ContentFile
import base64
from .serializers import EquipmentSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    def create(self, request, *args, **kwargs):

        image_b64 = request.data.get("inspection_image_base64")

        # Convert base64 → File
        if image_b64:
            try:
                img_data = base64.b64decode(image_b64)
                file = ContentFile(img_data, name="upload.jpg")

                request.data._mutable = True
                request.data["inspection_image"] = file
            except Exception as e:
                print("IMAGE ERROR:", e)

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

