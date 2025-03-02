from django.db import models
from django.conf import settings  # Use settings.AUTH_USER_MODEL for flexibility
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

# -------------------- Custom User Model --------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('artist', 'Artist'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='customer')

    # Fix reverse accessor issue
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True  # Only admins have staff privileges
        else:
            self.is_staff = False  # Artists and customers are not staff
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.role}"

class Artist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='artist_profile')
    bio = models.TextField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username
