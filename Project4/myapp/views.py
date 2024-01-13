from django.shortcuts import render, redirect
from django.contrib.auth import login  # Add this import
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LogoutView
from .forms import ReclamationForm
from .models import Reclamation
from django.contrib.auth.decorators import user_passes_test

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Use the imported login function
            return redirect('reclamation')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

# Logout view
@login_required
def custom_logout_view(request):
    # Perform logout
    LogoutView.as_view()(request)
    # Redirect to the login page
    return redirect('login')
'''
@login_required
def reclamation(request):
    if request.method == 'POST':
        form = ReclamationForm(request.POST)
        if form.is_valid():
            reclamation = form.save(commit=False)
            reclamation.user = request.user
            reclamation.save()
            messages.success(request, 'Reclamation submitted successfully.')
            return redirect('reclamation')
    else:
        form = ReclamationForm()

    reclamations = Reclamation.objects.filter(user=request.user)
    return render(request, 'myapp/reclamation.html', {'form': form, 'reclamations': reclamations})
'''

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def reclamation(request):
    reclamations = Reclamation.objects.select_related('user').all()

    if request.method == 'POST':
        form = ReclamationForm(request.POST)
        if form.is_valid():
            reclamation = form.save(commit=False)
            reclamation.user = request.user
            reclamation.save()
            messages.success(request, 'Reclamation submitted successfully.')
            return redirect('reclamation')
    else:
        form = ReclamationForm()

    return render(request, 'myapp/reclamation.html', {'form': form, 'reclamations': reclamations})