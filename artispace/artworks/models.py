from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Artist 

User = get_user_model()

class Artwork(models.Model):
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
