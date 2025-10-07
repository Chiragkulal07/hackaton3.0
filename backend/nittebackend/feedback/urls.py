# assessment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.feedback_view, name='feedback'),
]
