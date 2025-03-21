from django.urls import include, path
from app import views
from django.contrib.auth.views import LoginView

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('artist/home/', views.artistHome, name='artistHome'),
    path('artist/signup/', views.artist_signup, name='artist_signup'),
]
