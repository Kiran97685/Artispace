from django.urls import path, include
from django.contrib.auth.views import LoginView
from . import views
from django.contrib import admin

app_name = 'accounts'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),

    # General Registration Routes
    path('register/', views.register_view, name='user_register'),
    path('success/', views.success_view, name='success'),

    # Customer Routes
    path('signup/customer/', views.customer_signup, name="customer_signup"),
    path('login/customer/', views.customer_login, name='customer_login'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),

    # Artist Routes
    path('artist/signup/', views.artist_signup, name='artist_signup'),
    path('login/artist/', LoginView.as_view(template_name='accounts/artist_login.html'), name='artist_login'),
    path('dashboard/artist/', views.artist_dashboard, name='artist_dashboard'),

    # Default Login Route (for any user type)
    path('login/', views.login_view, name='login'),
    
]
