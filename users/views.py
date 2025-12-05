from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer, UserCreateUpdateSerializer

User = get_user_model()

class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    permission_classes = [IsAdminOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserListSerializer
        return UserCreateUpdateSerializer
    
    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({"message": "Status updated", "is_active": user.is_active})