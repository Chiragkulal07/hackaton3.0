from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=150, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    major = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.full_name or self.user.username

# Create your models here.
