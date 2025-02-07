from django.conf import settings
from django.db import models
from accounts.models import CustomUser

class Artist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='gallery_artist')
    bio = models.TextField(blank=True, null=True)  # Optional field for bio
    website_url = models.URLField(blank=True, null=True)  # Optional field for website URL

    def __str__(self):
        return f"{self.user.username} - Artist"


class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='artworks/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
