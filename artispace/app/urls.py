from django.urls import include, path
from app import views
from django.contrib.auth.views import LoginView

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('artist/home/', views.artistHome, name='artistHome'),
    path('login/', views.login_view, name='app_login'),
    path('artist/signup/', views.artist_signup, name='artist_signup'),
]
