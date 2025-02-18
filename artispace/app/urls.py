from django.urls import include, path
from app import views
from django.contrib.auth.views import LoginView

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='app_login'),  # Changed name to avoid conflicts
    path('artists/', views.artist_list, name='artist_list'),
    path('artworks/', views.artwork_list, name='artwork_list'),
    path('artist/signup/', views.artist_signup, name='artist_signup'),  # Add this line
]
