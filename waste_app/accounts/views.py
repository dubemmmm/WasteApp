from django.shortcuts import render
from django.urls import reverse, reverse_lazy, path, include
from django.views import generic 
from . import forms
# Create your views here.

class Signup(generic.CreateView):
    form_class = forms.UserCreateFrom
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
    
    
    