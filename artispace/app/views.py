from django.shortcuts import render
from .forms import ArtistSignupForm, UserSignupForm
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser

def home(request):
    return render(request, 'home.html')

def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

def some_gallery_view(request):
    return render(request, 'gallery/some_gallery_page.html')

def login_view(request):
    return render(request, 'accounts/registration/login.html')
def artist_list(request):
    # logic to fetch and display artists
    return render(request, 'app/artist_list.html')

def artwork_list(request):
    # Logic for fetching and displaying artwork data
    return render(request, 'app/artwork_list.html')

# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserSignupForm, ArtistSignupForm
from django.contrib.auth.decorators import login_required

def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('customer_dashboard')  # Redirect to user dashboard
    else:
        form = UserSignupForm()
    return render(request, 'accounts/user_signup.html', {'form': form})

def artist_signup(request):
    if request.method == 'POST':
        form = ArtistSignupForm(request.POST)
        if form.is_valid():
            artist = form.save()
            login(request, artist)
            return redirect('artist_dashboard')  # Redirect to artist dashboard
    else:
        form = ArtistSignupForm()
    return render(request, 'accounts/artist_signup.html', {'form': form})

class SignUpView(CreateView):
    model = CustomUser  # Or your custom user model
    template_name = 'accounts/signup.html'
    form_class = CustomUserCreationForm  # Or CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login page on successful sign-up
    
    
@login_required
def user_dashboard(request):
    if request.user.is_artist:
        return redirect('artist_dashboard')  # Prevent artists from accessing user dashboard
    return render(request, 'accounts/user_dashboard.html')

@login_required
def artist_dashboard(request):
    if not request.user.is_artist:
        return redirect('user_dashboard')  # Prevent users from accessing artist dashboard
    return render(request, 'accounts/artist_dashboard.html')
