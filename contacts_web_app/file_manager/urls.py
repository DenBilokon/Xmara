from django.urls import path, include

from .views import main_mf, images

app_name = "file_manager"

urlpatterns = [
    path('', main_mf, name='main_mf'),
    path('images/', images, name='images'),
]
