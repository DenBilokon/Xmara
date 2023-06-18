from django.urls import path

from . import views

app_name = "file_manager"

urlpatterns = [
    path('', views.main_mf, name='main_mf'),
    path('page/<int:page>/', views.main_mf, name='root_paginate'),
    path('picture/', views.upload_picture, name='upload_picture'),
    path('picture/delete/<int:picture_id>/', views.delete_picture, name='delete_picture'),
    path('picture/search_picture/', views.search_picture, name='search_picture'),
    path('document/', views.upload_document, name='upload_document'),
    path('document/delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('document/search_document/', views.search_document, name='search_document'),
    path('video/', views.upload_video, name='upload_video'),
    path('video/delete/<int:video_id>/', views.delete_video, name='delete_video'),
    path('video/search_video/', views.search_video, name='search_video'),
    path('audio/', views.upload_audio, name='upload_audio'),
    path('audio/delete/<int:audio_id>/', views.delete_audio, name='delete_audio'),
    path('audio/search_audio/', views.search_audio, name='search_audio'),
    path('archive/', views.upload_archive, name='upload_archive'),
    path('archive/delete/<int:archive_id>/', views.delete_archive, name='delete_archive'),
    path('archive/search_archive/', views.search_archive, name='search_archive'),
    path('download_image/<path:image_url>/', views.download_image, name='download_image'),

]
