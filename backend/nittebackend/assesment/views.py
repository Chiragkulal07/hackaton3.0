from django.shortcuts import render
from django.http import HttpResponse

# Default home page view
def home(request):
    return HttpResponse("Welcome to the Career Readiness Assistant Home Page!")