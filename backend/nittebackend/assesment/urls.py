# assessment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_assessment_questions, name='home'),  # default route ("/assessment/")
]
