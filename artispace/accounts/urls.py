from django.urls import path, include
from django.contrib.auth.views import LoginView
from . import views
from django.contrib import admin

app_name = 'accounts'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('register/', views.register_view, name='user_register'),
    
    # Signup routes
    path('signup/artist/', views.artist_signup, name='artist_signup'),
    path('customer/signup/', views.customer_signup, name='customer_signup'),
    path('customer/login/', views.customer_login, name='customer_login'),
    
    # Login routes
    path('login/artist/', LoginView.as_view(template_name='accounts/artist_login.html'), name='artist_login'),
    path('login/customer/', LoginView.as_view(template_name='accounts/customer_login.html'), name='customer_login'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # Dashboard routes
    path('dashboard/artist/', views.artist_dashboard, name='artist_dashboard'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
]
