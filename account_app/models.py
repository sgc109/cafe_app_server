from django.db import models
from django.utils import timezone
import os

class Profile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True)
