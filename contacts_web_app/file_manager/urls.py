from django.urls import path, include

from .views import main_mf, upload_picture, upload_document, upload_video, upload_audio, gallery, download_image, \
    delete_picture

app_name = "file_manager"

urlpatterns = [
    path('', main_mf, name='main_mf'),
    path('page/<int:page>/', main_mf, name='root_paginate'),
    path('picture/', upload_picture, name='upload_picture'),
    path('delete/<int:picture_id>', delete_picture, name='delete'),
    path('documents/', upload_document, name='upload_document'),
    path('video/', upload_video, name='upload_video'),
    path('audio/', upload_audio, name='upload_audio'),
    path('gallery/', gallery, name='gallery'),
    path('download_image/<path:image_url>/', download_image, name='download_image'),

]
