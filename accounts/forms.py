from django import forms
from django.contrib.auth.models import User
from django.contrib import auth


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=20) 
    
    def clean_username(self):
        user = User.objects.filter(username__exact=self.cleaned_data['username'].lower())
        if not user:
            return self.cleaned_data['username'].lower()
        raise forms.ValidationError('Username already exists.')
 
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  

    def clean(self):
        
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            username = username.lower()
            user = auth.authenticate(username=username, password=password)
            if not user or not user.is_active:
               raise forms.ValidationError('Username and password not match.')

        return self.cleaned_data

