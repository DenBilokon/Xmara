from django.urls import path, include

from .views import main_mf, images, upload_document, upload_video

app_name = "file_manager"

urlpatterns = [
    path('', main_mf, name='main_mf'),
    path('images/', images, name='images'),
    path('documents/', upload_document, name='upload_document'),
    path('video/', upload_video, name='upload_video'),
]
