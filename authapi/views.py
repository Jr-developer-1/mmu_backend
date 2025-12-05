from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import AppUser
import json

@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)
    username = data.get("username")
    password = data.get("password")

    try:
        user = AppUser.objects.get(username=username)
    except AppUser.DoesNotExist:
        return JsonResponse({"success": False, "message": "Invalid username"}, status=401)

    if not user.check_password(password):
        return JsonResponse({"success": False, "message": "Invalid password"}, status=401)

    # 🔵 ADD THIS CHECK
    if not user.is_active:
        return JsonResponse({
            "success": False,
            "message": "Account disabled. Contact admin."
        }, status=403)

    return JsonResponse({
        "success": True,
        "username": user.username,
        "role": user.role
    })