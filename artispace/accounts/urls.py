from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.contrib import admin
from . import views
from .views import (
    artist_register,
    artist_signup,
    artist_login,
    artist_dashboard,
    customer_signup,
    customer_login,
    customer_dashboard,
    home,
)

app_name = 'accounts'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),

    # Customer Routes
    path('customer_signup/', views.customer_signup, name='customer_signup'),
    path('login/customer/', views.customer_login, name='customer_login'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('artist/dashboard/', views.artist_dashboard, name='artist_dashboard'),

    # Artist Routes
    path('artist/signup/', views.artist_signup, name='artist_signup'),
    path('login/artist/', LoginView.as_view(template_name='accounts/artist_login.html'), name='artist_login'),

    # Default Login Route (for any user type)
    path('login/', views.login_view, name='login'),
    
]
