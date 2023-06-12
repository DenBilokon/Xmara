from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone


class Picture(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    image = CloudinaryField(resource_type='image')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Document(models.Model):
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Video(models.Model):
    title = models.CharField(max_length=255)
    video = CloudinaryField(resource_type='video')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
