from django.shortcuts import render
from .forms import ArtistSignupForm, UserSignupForm
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'app/home.html')

def artistHome(request):
    return render(request, 'app/artistHome.html')

def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

def artist_dashboard(request):
    return render(request, "accounts/artist_dashboard.html")

def login_view(request):
    return render(request, 'accounts/registration/login.html')

# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserSignupForm, ArtistSignupForm


def customer_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('customer_dashboard')
    else:
        form = UserSignupForm()
    return render(request, 'accounts/customer_signup.html', {'form': form})

def artist_signup(request):
    if request.method == 'POST':
        form = ArtistSignupForm(request.POST)
        if form.is_valid():
            artist = form.save()
            login(request, artist)
            return redirect('accounts/artist_dashboard')  # Redirect to artist dashboard
    else:
        form = ArtistSignupForm()
    return render(request, 'accounts/artist_signup.html', {'form': form})

class SignUpView(CreateView):
    model = CustomUser  # Or your custom user model
    template_name = 'accounts/signup.html'
    form_class = CustomUserCreationForm  # Or CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login page on successful sign-up
    
    
#@login_required
#def user_dashboard(request):
 #  if request.user.is_artist:
  #      return redirect('accounts/artist_dashboard')  # Prevent artists from accessing user dashboard
   # return render(request, 'accounts/user_dashboard.html')

@login_required
def artist_dashboard(request):
    print("Rendering artist_dashboard.html")  # Debugging
    return render(request, 'accounts/artist_dashboard.html')