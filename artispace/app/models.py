from django.db import models
from accounts.models import CustomUser
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Artist Model

class Artist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='app_artist')
    bio = models.TextField()  # Add artist bio
    website_url = models.URLField(blank=True, null=True)  # Add artist's website URL

    def __str__(self):
        return self.user.username

class CustomUser(AbstractUser):
    is_artist = models.BooleanField(default=False)  # Add this field
    is_customer = models.BooleanField(default=False)  # Optional if needed

    def __str__(self):
        return self.username