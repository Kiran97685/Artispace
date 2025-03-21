from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.http import JsonResponse
import json
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django import forms
from .models import CustomUser, Artist
from django.contrib import messages
from .forms import (
    ArtistForm, 
    ArtistSignUpForm, 
    CustomerSignUpForm,
    LoginForm, 
)
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages  # Import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.middleware.csrf import get_token

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
            return redirect('accounts:artist_dashboard')  # Replace with actual URL

    else:
        user_form = ArtistSignUpForm()
        artist_form = ArtistForm()

    return render(request, 'accounts/artist_signup.html', {
        'user_form': user_form, 'artist_form': artist_form
    })

def artist_signup(request):
    logout(request)  # Log out any currently logged-in user
    request.session.flush()  # Clear session data
    if request.method == "POST":
        user_form = ArtistSignUpForm(request.POST)
        artist_form = ArtistForm(request.POST)

        if user_form.is_valid() and artist_form.is_valid():
            # Save the user
            user = user_form.save(commit=False)
            user.role = 'artist'
            user.set_password(user.password)
            user.save()  # Save user first

            # Save the artist profile
            artist = artist_form.save(commit=False)
            artist.user = user  # Link the artist profile to the user
            artist.save()  # Save artist profile
            messages.success(request, "Signed up successfully!")  # Add success message
            return redirect("app:artistHome")

    else:
        user_form = ArtistSignUpForm()
        artist_form = ArtistForm()

    return render(request, "app/artistHome.html", {"user_form": user_form, "artist_form": artist_form})


def artist_login(request):
    login_error = None  # Store login error separately
    show_modal = False  # Default: Do not show modal
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == 'artist':  # Check if the user is an artist
                login(request, user)
                request.session['user_type'] = 'artist'  # Store user type in session
                request.session.set_expiry(0)  # Persist session until logout
                
                return redirect(reverse_lazy('accounts:artist_dashboard'))
            else:
                login_error = "Access Denied: You are not an artist."
        else:
            login_error = "Invalid username or password."
            show_modal = True  # Keep modal open if login fails
            context = {
            'login_error': login_error,
            'show_modal': show_modal,  # Keep the modal open
            'csrf_token': get_token(request)  # Ensure CSRF token is regenerated
    }
            return render(request, 'app/artistHome.html')

    return render(request, 'accounts/artist_login.html', context)

# -------------------- Customer Signup --------------------

def customer_signup(request):
    if request.method == "POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.role = 'customer'
            user.set_password(user.password)
            user.save()  # Save user first
            messages.success(request, "Signed up successfully!")  # Add success message
            return redirect("app:home")  # Redirect to the login page
    else:
        form = CustomerSignUpForm()
    return render(request, "app/home.html", {"form": form})

# -------------------- Customer Login --------------------
def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
       
        if user is not None:
            if user.role == 'customer':  # Check if the user is a customer
                login(request, user)
                request.session['user_type'] = 'customer'  # Store user type in session
                request.session.set_expiry(0)  # Persist session until logout

                return redirect('accounts:customer_dashboard')
            else:
                messages.error(request, "Access Denied: You are not a customer.", extra_tags="login_error")
        else:
            messages.error(request, "Invalid username or password.", extra_tags="login_error")
            return render(request, 'app/home.html')  # Ensure correct template path

    return render(request, 'accounts/artist_login.html')



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

@login_required
def customer_dashboard(request):
    
    if request.session.get('user_type') == 'customer':
        return render(request, "customer_dashboard.html")
    
    return redirect('customer_login')

@login_required
def artist_dashboard(request):
    if request.session.get('user_type') == 'artist':
        return render(request, "accounts/artist_dashboard.html")  # ✅ Correct template path
    else:
        return redirect('accounts:artist_login')  # ✅ Redirect to the artist login page


def artist_logout(request):
    if 'user_type' in request.session:
        del request.session['user_type']  # Remove user type
    request.session.flush()  # Completely clear the session
    logout(request)  # Logout user
    return redirect('app:artistHome')  # Redirect to artist login

def customer_logout(request):
    if 'user_type' in request.session:
        del request.session['user_type']  # Delete user type from session
    request.session.flush()  # Completely clear the session
    logout(request)  # Logout the user
    return redirect('app:home')  # Redirect to login page
 
# -------------------- Home Page --------------------
def home(request):
    return render(request, 'app/home.html')

def artistHome(request):
    return render(request, 'artistHome.html')

def customer_dashboard(request):
    return render(request, "accounts/customer_dashboard.html")