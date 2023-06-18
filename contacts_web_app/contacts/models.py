from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class File(models.Model):
    file = models.FileField(upload_to='files')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.file}'


class Contacts(models.Model):
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    phone = PhoneNumberField()
    email = models.EmailField(null=False, default="example@email.com")
    birthday = models.CharField(max_length=15, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.firstname}, {self.lastname}, {self.phone}, {self.email}, {self.birthday}'
