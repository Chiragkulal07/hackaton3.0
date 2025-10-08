from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json


def home(request):
    return JsonResponse({"message": "Users API is running"})


@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        return HttpResponseBadRequest("username and password required")
    if User.objects.filter(username=username).exists():
        return HttpResponseBadRequest("User exists")
    user = User.objects.create_user(username=username, password=password)
    return JsonResponse({"id": user.id, "username": user.username})


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")
    username = payload.get("username")
    password = payload.get("password")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return HttpResponseBadRequest("Invalid credentials")
    login(request, user)
    return JsonResponse({"id": user.id, "username": user.username})


def logout_user(request):
    logout(request)
    return JsonResponse({"status": "ok"})


def me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False})
    return JsonResponse({"authenticated": True, "username": request.user.username, "id": request.user.id})