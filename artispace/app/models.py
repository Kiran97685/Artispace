from django.db import models
from accounts.models import CustomUser
from django.conf import settings


# Artist Model

class Artist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='app_artist')
    bio = models.TextField()  # Add artist bio
    website_url = models.URLField(blank=True, null=True)  # Add artist's website URL

    def __str__(self):
        return self.user.username

class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    artist = models.ForeignKey(
        'app.Artist',  # Reference the Artist model
        on_delete=models.CASCADE,
        related_name='app_artworks'  # Unique related_name
    )
    image = models.ImageField(upload_to='artworks/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
