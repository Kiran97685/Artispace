from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('artists/', views.artist_list, name='artist_list'),
    path('index/', views.index, name='index'),
    path('some-gallery/', views.some_gallery_page, name='some_gallery_page'), 
]
