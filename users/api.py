from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from users.models import AppUser
import json

# Get all users
def get_users(request):
    users = AppUser.objects.values("id", "username", "role", "is_active")
    return JsonResponse(list(users), safe=False)


# Create new user
@csrf_exempt
def create_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if AppUser.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    u = AppUser(username=username, role=role)
    u.set_password(password)

    return JsonResponse({"success": True, "message": "User created"})


# (Optional) Deactivate user
@csrf_exempt
def toggle_active(request, user_id):
    try:
        user = AppUser.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        return JsonResponse({"success": True})
    except AppUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
