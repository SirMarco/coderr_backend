from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    TYPE_CHOICES = [
        ("customer", "Customer"),
        ("business", "Business"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file = models.ImageField(upload_to="profile_pics/", blank=True, default="")
    location = models.CharField(max_length=50, blank=True, default="")
    tel = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return f"{self.user.username} - {self.type}"
