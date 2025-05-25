from django.shortcuts import render, redirect
from django.conf import settings
from .models import Artwork
from accounts.models import Artist
import boto3
import uuid

# View to upload an artwork
def upload_artwork(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        image_file = request.FILES.get('image')

        artist_id = request.session.get('artist_id')
        if not artist_id:
            return render(request, 'artworks/upload_artwork.html', {'error': 'You must be logged in as an artist.'})

        try:
            artist = Artist.objects.get(id=artist_id)
        except Artist.DoesNotExist:
            return render(request, 'artworks/upload_artwork.html', {'error': 'Invalid artist session.'})

        if not image_file:
            return render(request, 'artworks/upload_artwork.html', {'error': 'Please select an image file.'})

        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )

            file_extension = image_file.name.split('.')[-1]
            s3_key = f'artworks/{uuid.uuid4()}.{file_extension}'

            s3.upload_fileobj(
                image_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                s3_key,
            )

            image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}"

            Artwork.objects.create(
                title=title,
                price=float(price) if price else 0.0,
                image=image_url,
                artist=artist
            )

            return redirect('artwork_list')  # <-- This will redirect to view artworks page

        except Exception as e:
            return render(request, 'artworks/upload_artwork.html', {
                'error': f'Upload failed: {str(e)}'
            })

    return render(request, 'artworks/upload_artwork.html')

# View to display artworks uploaded by the logged-in artist
def artwork_list(request):
    artist_id = request.session.get('artist_id')
    if not artist_id:
        return render(request, 'artworks/artwork_list.html', {'error': 'You must be logged in as an artist.'})
        print("Artist ID from session:", artist_id)

    try:
        artist = Artist.objects.get(id=artist_id)
    except Artist.DoesNotExist:
        return render(request, 'artworks/artwork_list.html', {'error': 'Invalid artist session.'})

    artworks = Artwork.objects.filter(artist=artist)
    print("Found artworks:", artworks)
    return render(request, 'artworks/artwork_list.html', {'artworks': artworks})
