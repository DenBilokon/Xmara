from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone


extensions_img = ['jpeg', 'png', 'jpg', 'svg']
extensions_doc = ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']
extensions_video = ['avi', 'mp4', 'mov', 'mkv']
extensions_music = ['mp3', 'ogg', 'wav', 'amr']
extensions_archives = ['zip', 'gz', 'tar', 'rar']


class Picture(models.Model):
    title = models.CharField(max_length=255, default='Unknown')
    image = CloudinaryField(resource_type='auto', allowed_formats=extensions_img, folder='pictures')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Document(models.Model):
    title = models.CharField(max_length=255, default='Unknown')
    document = CloudinaryField(resource_type='auto', allowed_formats=extensions_doc, folder='documents')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Video(models.Model):
    title = models.CharField(max_length=255, default='Unknown')
    video = CloudinaryField(resource_type='auto', allowed_formats=extensions_video, folder='video')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Audio(models.Model):
    artist = models.CharField(max_length=50, default='Unknown', null=True)
    title = models.CharField(max_length=100, default='Unknown')
    audio = CloudinaryField(resource_type='auto', allowed_formats=extensions_music, folder='audio')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Archive(models.Model):
    title = models.CharField(max_length=100, default='Unknown')
    archive = CloudinaryField(resource_type='auto', allowed_formats=extensions_archives, folder='archives')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)



