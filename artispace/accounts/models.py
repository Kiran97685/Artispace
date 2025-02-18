from django.db import models
from django.conf import settings  # Use settings.AUTH_USER_MODEL for flexibility
from django.contrib.auth.models import AbstractUser

# -------------------- Custom User Model --------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('artist', 'Artist'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='customer')

    def save(self, *args, **kwargs):
        # Ensure only Admins are staff users
        if self.role == 'admin':
            self.is_staff = True  # Only admin has staff privileges
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
# -------------------- Artwork Model --------------------
class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    artist = models.ForeignKey(
        Artist,  # Direct reference instead of string
        on_delete=models.CASCADE,
        related_name='artworks'
    )
    image = models.ImageField(upload_to='artworks/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
