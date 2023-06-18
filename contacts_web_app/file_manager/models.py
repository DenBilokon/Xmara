from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone


class Picture(models.Model):
    title = models.CharField(max_length=255)
    image = CloudinaryField(resource_type='image')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Document(models.Model):
    title = models.CharField(max_length=255)
    document = CloudinaryField(resource_type='auto')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Video(models.Model):
    title = models.CharField(max_length=255)
    video = CloudinaryField(resource_type='video')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Audio(models.Model):
    artist = models.CharField(max_length=50, default='Unknown', null=True)
    title = models.CharField(max_length=100, default=None)
    audio = CloudinaryField(resource_type='auto')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    # def delete(self, *args, **kwargs):
    #     # Видаляємо аудіофайл з Cloudinary
    #     self.audio.delete()
    #
    #     # Видаляємо запис з бази даних
    #     super().delete(*args, **kwargs)



