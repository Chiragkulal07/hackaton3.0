from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

from .models import Feedback


def home(request):
    return JsonResponse({"message": "Feedback API is running"})


@csrf_exempt
def submit_feedback(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    username = payload.get("username")
    message = payload.get("message")
    rating = payload.get("rating", 5)
    if not message:
        return HttpResponseBadRequest("message required")

    user = None
    if username:
        user, _ = User.objects.get_or_create(username=username)
    rating_int = max(1, min(5, int(rating)))
    fb = Feedback.objects.create(user=user, message=message, rating=rating_int)
    return JsonResponse({"id": fb.id, "status": "ok"})
from django.http import HttpResponse

# Default home page view
def home(request):
    return HttpResponse("Welcome to the Career Readiness Assistant feedback Page!")