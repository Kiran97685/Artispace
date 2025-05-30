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
        print("Received POST:", title, price, image_file)

        artist_id = request.session.get('artist_id')
        print("Artist ID from session:", artist_id)

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
            print("Uploading to S3 as:", s3_key)

            s3.upload_fileobj(
                image_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                s3_key,
            )

            image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}"
            print("Image URL:", image_url)

            # Save to DB
            artwork = Artwork.objects.create(
                title=title,
                price=float(price) if price else 0.0,
                image=image_url,
                artist=artist
            )
            print("Artwork saved:", artwork)

            return render(request, 'artworks/upload_artwork.html', {
                'success': 'Artwork uploaded successfully.'
            })

        except Exception as e:
            print("Upload failed:", str(e))
            return render(request, 'artworks/upload_artwork.html', {
                'error': f'Upload failed: {str(e)}'
            })

    return render(request, 'artworks/upload_artwork.html')

# View to display artworks uploaded by the logged-in artist
def artwork_list(request):
    # Get the artist from the session
    artist_id = request.session.get('artist_id')
    if not artist_id:
        return render(request, 'artworks/artwork_list.html', {'error': 'You must be logged in as an artist.'})

    try:
        artist = Artist.objects.get(id=artist_id)
    except Artist.DoesNotExist:
        return render(request, 'artworks/artwork_list.html', {'error': 'Invalid artist session.'})

    # Filter artworks by the logged-in artist
    artworks = Artwork.objects.filter(artist=artist)
    return render(request, 'artworks/artwork_list.html', {'artworks': artworks})
