from django.urls import path
from .views import upload_file, home

app_name = 'app'
urlpatterns = [
    path('home', home, name='home'),
    path('upload', upload_file, name='upload')
    
]