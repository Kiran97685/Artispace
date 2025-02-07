from django.shortcuts import render
from .models import Artist, Artwork

def artist_list(request):
    artists = Artist.objects.all()
    return render(request, 'gallery/artist_list.html', {'artists': artists})

def artwork_list(request):
    artworks = Artwork.objects.all()
    return render(request, 'gallery/artwork_list.html', {'artworks': artworks})

def index(request):
    return render(request, 'gallery/index.html')

def some_gallery_page(request):
    # Your view logic here
    return render(request, 'gallery/some_gallery_page.html')