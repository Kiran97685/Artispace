from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django import forms
from .models import CustomUser, Artist  # Ensure the correct model is imported
from .forms import (
    CustomUserCreationForm, 
    ArtistForm, 
    ArtistSignUpForm, 
    UserSignUpForm, 
    CustomerSignUpForm, 
    LoginForm, 
    RegistrationForm
)

# Get the custom user model
CustomUser = get_user_model()

# Artist Registration
def artist_register(request):
    if request.method == 'POST':
        user_form = ArtistSignUpForm(request.POST, request.FILES)
        artist_form = ArtistForm(request.POST, request.FILES)
        if user_form.is_valid() and artist_form.is_valid():
            user = user_form.save()
            artist = artist_form.save(commit=False)
            artist.user = user
            artist.save()
            login(request, user)
            return redirect('artist-dashboard')  
    else:
        user_form = ArtistSignUpForm()
        artist_form = ArtistForm()

    return render(request, 'accounts/artist_signup.html', {'user_form': user_form, 'artist_form': artist_form})

def artist_signup(request):
    if request.method == 'POST':
        form = ArtistSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  # Redirect after signup
    else:
        form = ArtistSignUpForm()

    return render(request, 'accounts/artist_signup.html', {'form': form})

# Customer Signup
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

# Customer Login
def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid credentials, please try again."
            return render(request, 'accounts/customer_login.html', {'error_message': error_message})
    
    return render(request, 'accounts/customer_login.html')

# General Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

# General User Registration
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

# Home Page
def home(request):
    return render(request, 'app/home.html')

# Dashboards
def artist_dashboard(request):
    return render(request, 'accounts/artist_dashboard.html')

def customer_dashboard(request):
    return render(request, 'user-dashboard.html')

def user_dashboard(request):
    return render(request, 'accounts/user-dashboard.html')

def some_gallery_view(request):
    return render(request, 'some_gallery_page.html')
