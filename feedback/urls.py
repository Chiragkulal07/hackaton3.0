# assessment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='feedback_home'),
    path('submit/', views.submit_feedback, name='feedback_submit'),
]
