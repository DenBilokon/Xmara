from django.urls import path, include

from .views import main_mf

app_name = "file_manager"

urlpatterns = [
    path('', main_mf, name='main_mf'),
]
