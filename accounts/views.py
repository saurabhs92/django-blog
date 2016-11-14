from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.shortcuts import render

def login_view(request):
    return render(request, 'accounts/form.html', {})

def register_view(request):
    return render(request, 'accounts/form.html', {})

def logout_view(request):
    return render(request, 'accounts/form.html', {})
