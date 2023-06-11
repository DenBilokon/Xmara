from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone


class Library(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    image = CloudinaryField('image')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
