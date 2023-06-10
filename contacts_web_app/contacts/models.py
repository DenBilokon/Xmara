from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class Contacts(models.Model):
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    phone = PhoneNumberField()
    email = models.EmailField(unique=True, null=False)
    birthday = models.CharField(max_length=15, null=False)

    def __str__(self):
        return f'{self.firstname}, {self.lastname}, {self.phone}, {self.email}, {self.birthday}'
