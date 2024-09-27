from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth import logout
class LandingPage(generic.TemplateView):
    template_name='landing.html'
    
class HomePage(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home.html'
    
class LogoutPage(generic.TemplateView):
    template_name = 'landing.html'
    
    def get(self, request, *args, **kwargs):
        # Log out the user
        logout(request) 
        return render(request, self.template_name)
    
    