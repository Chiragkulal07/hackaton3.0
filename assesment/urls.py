# assessment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='assesment_home'),
    path('questions/', views.get_questions, name='assesment_questions'),
    path('submit/', views.submit_assessment, name='assesment_submit'),
    path('profile/<str:username>/', views.get_profile, name='assesment_profile'),
]
