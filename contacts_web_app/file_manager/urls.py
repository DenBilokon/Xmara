from django.urls import path, include

from .views import main_mf, upload_picture, upload_document, upload_video, upload_audio, gallery

app_name = "file_manager"

urlpatterns = [
    path('', main_mf, name='main_mf'),
    path('picture/', upload_picture, name='upload_picture'),
    path('documents/', upload_document, name='upload_document'),
    path('video/', upload_video, name='upload_video'),
    path('audio/', upload_audio, name='upload_audio'),
    path('gallery/', gallery, name='gallery')
]
