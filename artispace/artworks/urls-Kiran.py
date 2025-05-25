from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_artwork, name='upload_artwork'),
    path('list/', views.artwork_list, name='artwork_list'),
    path('my-artworks/', views.artwork_list, name='artwork_list'),
]
