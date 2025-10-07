# accounts/models.py
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    major = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.full_name or self.user.username

class User(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.email
