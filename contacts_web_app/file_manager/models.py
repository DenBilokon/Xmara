from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone


EXTENSIONS_IMG = ['jpeg', 'png', 'jpg', 'svg', 'gif']
EXTENSIONS_DOC = ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'py', 'csv', 'css', 'html', 'js']
EXTENSIONS_VIDEO = ['avi', 'mp4', 'mov', 'mkv']
EXTENSIONS_MUSIC = ['mp3', 'ogg', 'wav', 'amr']
EXTENSIONS_ARCHIVES = ['zip', 'gz', 'tar', '7z']


class Picture(models.Model):
    title = models.CharField(max_length=255, default='Unknown')
    image = CloudinaryField(resource_type='auto', allowed_formats=EXTENSIONS_IMG, folder='pictures')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Document(models.Model):
    title = models.CharField(max_length=255, default='Unknown')
    document = CloudinaryField(resource_type='auto', allowed_formats=EXTENSIONS_DOC, folder='documents')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Video(models.Model):
    title = models.CharField(max_length=255, default='Unknown')
    video = CloudinaryField(resource_type='auto', allowed_formats=EXTENSIONS_VIDEO, folder='video')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Audio(models.Model):
    artist = models.CharField(max_length=50, default='Unknown', null=True)
    title = models.CharField(max_length=100, default='Unknown')
    audio = CloudinaryField(resource_type='auto', allowed_formats=EXTENSIONS_MUSIC, folder='audio')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Archive(models.Model):
    title = models.CharField(max_length=100, default='Unknown')
    archive = CloudinaryField(resource_type='auto', allowed_formats=EXTENSIONS_ARCHIVES, folder='archives')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
