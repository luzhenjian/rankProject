from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.core.urlresolvers import reverse
from .forms import *


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            
            new_user = auth.authenticate(username=username,password=password)
            auth.login(request, new_user)
            redirect = request.REQUEST.get('next')
            if redirect: 
                return HttpResponseRedirect(redirect)
            else:
                return HttpResponseRedirect(reverse('rank'))
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form,})
    
    
def login(request): 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            auth.login(request, user)
            redirect = request.REQUEST.get('next')
            if redirect: 
                return HttpResponseRedirect(redirect)
            else:
                return HttpResponseRedirect(reverse('rank'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form,})
    
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('rank'))

