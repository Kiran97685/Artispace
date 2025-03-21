from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.contrib import admin
from . import views 
from .views import artist_logout

app_name = 'accounts'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),

    path('artist/signup/', views.artist_signup, name='artist_signup'),
    path('customer/signup/', views.customer_signup, name='customer_signup'),
    
    path('login/artist/', views.artist_login, name='artist_login'),
    path('login/customer/', views.customer_login, name='customer_login'),
    
    path('artist/dashboard/', views.artist_dashboard, name='artist_dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),

    path("artist/logout/", views.artist_logout, name="artist_logout"),
    path("customer/logout/", views.customer_logout, name="customer_logout"),
]
