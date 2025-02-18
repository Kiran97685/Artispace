from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),  # Main app
    path("accounts/", include("accounts.urls", namespace="accounts")), # Accounts app
    # path('gallery/', include(('gallery.urls', 'gallery'))),  # Gallery app (commented for now)
    path('', RedirectView.as_view(url='/app/', permanent=False)),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
