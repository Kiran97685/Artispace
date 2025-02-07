# Migration file
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='profile_image',
            field=models.ImageField(
                blank=True,
                default='artists/default_image.png',  # Relative to MEDIA_ROOT
                null=True,
                upload_to='artists/'
            ),
        ),
    ]
