from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.

class UserProfileModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    user_registration_code = models.CharField(max_length=8, help_text=('For your email was sent registration code,'
                                                                       'please enter this code in the field'), )

    def __str__(self):
        return f'user profile model of {self.user.username}'
