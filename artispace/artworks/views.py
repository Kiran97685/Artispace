from django.shortcuts import render, redirect
from django.conf import settings
from .models import Artwork
from accounts.models import Artist
import boto3
import uuid

def upload_artwork(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        image_file = request.FILES.get('image')
        
        artist_id = request.session.get('artist_id')
        if not artist_id:
            return render(request, 'upload_artwork.html', {'error': 'You must be logged in as an artist.'})

        try:
             artist = Artist.objects.get(user=request.user)
        except Artist.DoesNotExist:
            return render(request, 'upload_artwork.html', {'error': 'Invalid artist.'})

        # Upload image to S3
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

        # Save artwork
        price = float(price) if price else 0.0
        Artwork.objects.create(title=title, price=price, image=image_url, artist=artist)

        return render(request, 'upload_artwork.html', {'success': 'Artwork uploaded successfully.'})

    return render(request, 'upload_artwork.html')

def artwork_list(request):
    artworks = Artwork.objects.all()  # or [] if no model yet
    return render(request, 'artworks/artwork_list.html', {'artworks': artworks})