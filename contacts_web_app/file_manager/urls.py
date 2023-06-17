from django.urls import path

from .views import main_mf, upload_picture, upload_document, upload_video, upload_audio, gallery, download_image, \
    delete_picture, delete_audio, delete_video, delete_document

app_name = "file_manager"

urlpatterns = [
    path('', main_mf, name='main_mf'),
    path('page/<int:page>/', main_mf, name='root_paginate'),
    path('picture/', upload_picture, name='upload_picture'),
    path('picture/delete/<int:picture_id>/', delete_picture, name='delete_picture'),
    path('document/', upload_document, name='upload_document'),
    path('document/delete/<int:document_id>/', delete_document, name='delete_document'),
    path('video/', upload_video, name='upload_video'),
    path('video/delete/<int:video_id>/', delete_video, name='delete_video'),
    path('audio/', upload_audio, name='upload_audio'),
    path('audio/delete/<int:audio_id>/', delete_audio, name='delete_audio'),
    path('gallery/', gallery, name='gallery'),
    path('download_image/<path:image_url>/', download_image, name='download_image'),

]
