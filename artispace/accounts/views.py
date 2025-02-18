from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django import forms
from .models import CustomUser, Artist  # Ensure the correct model is imported
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import (
    CustomUserCreationForm, 
    ArtistForm, 
    ArtistSignUpForm, 
    CustomerSignUpForm,
    LoginForm, 
    RegistrationForm
)
from django.db import IntegrityError
from django.contrib.auth.models import User

# Get the custom user model
CustomUser = get_user_model()

# -------------------- Artist Registration --------------------
def artist_register(request):
    if request.method == 'POST':
        # Get form data
        user_form = ArtistSignUpForm(request.POST, request.FILES)
        artist_form = ArtistForm(request.POST, request.FILES)
        
        if user_form.is_valid() and artist_form.is_valid():
            # Save user first
            user = user_form.save(commit=False)
            user.role = 'artist'  # Set the user role to artist
            user.save()  # Save user
            
            # Create artist profile
            artist = artist_form.save(commit=False)
            artist.user = user
            artist.save()

            # Log the user in and redirect to artist dashboard
            login(request, user)
            return redirect('artist-dashboard')  # Replace with actual URL

    else:
        user_form = ArtistSignUpForm()
        artist_form = ArtistForm()

    return render(request, 'accounts/artist_signup.html', {
        'user_form': user_form, 'artist_form': artist_form
    })

def artist_signup(request):
    if request.method == "POST":
        user_form = ArtistSignUpForm(request.POST)
        artist_form = ArtistForm(request.POST)

        if user_form.is_valid() and artist_form.is_valid():
            # Save the user
            user = user_form.save(commit=False)
            user.role = 'artist'
            user.save()  # Save user first

            # Save the artist profile
            artist = artist_form.save(commit=False)
            artist.user = user  # Link the artist profile to the user
            artist.save()  # Save artist profile

            return redirect("accounts:artist_login")  # Redirect to the login page

    else:
        user_form = ArtistSignUpForm()
        artist_form = ArtistForm()

    return render(request, "accounts/artist_signup.html", {"user_form": user_form, "artist_form": artist_form})

def artist_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if hasattr(user, 'artist'):  # Check if the user is an artist
                return redirect('artist-dashboard')
            else:
                return redirect('customer-dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'accounts/artist_login.html')

# -------------------- Customer Signup --------------------

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            # Process the form data
            form.save()
            return redirect('accounts:success')  # Redirect to success page after form submission
    else:
        form = CustomerSignUpForm()
    
    return render(request, 'accounts/customer_signup.html', {'form': form})

# -------------------- Customer Login --------------------
def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'accounts/customer_login.html')

# -------------------- Username Validation --------------------
def clean_username(self):
    username = self.cleaned_data.get('username')

    # Check if the username exists in the Artist model (related to CustomUser)
    if Artist.objects.filter(user__username=username).exists():
        raise ValidationError("A user with this username already exists in the Artist account.")

    # Check if the username exists in the CustomUser model (for Customer accounts)
    if CustomUser.objects.filter(username=username).exists():
        raise ValidationError("A user with this username already exists in the Customer account.")
    
    return username

# -------------------- General Login View --------------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # You can handle form submission and login logic here
            print(form.cleaned_data)
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

# -------------------- General User Registration --------------------
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            return redirect('app:index')  
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# -------------------- Home Page --------------------
def home(request):
    return render(request, 'app/home.html')

# -------------------- Dashboards --------------------
def artist_dashboard(request):
    return render(request, 'accounts/artist_dashboard.html')

def customer_dashboard(request):
    return render(request, 'user-dashboard.html')

def user_dashboard(request):
    return render(request, 'accounts/user-dashboard.html')

def some_gallery_view(request):
    return render(request, 'some_gallery_page.html')

def success_view(request):
    return render(request, 'accounts/success.html')
