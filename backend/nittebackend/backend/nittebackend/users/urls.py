# assessment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='users_home'),
    path('register/', views.register_user, name='users_register'),
    path('login/', views.login_user, name='users_login'),
    path('logout/', views.logout_user, name='users_logout'),
    path('me/', views.me, name='users_me'),
]
