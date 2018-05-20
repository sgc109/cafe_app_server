from django.db import models
from django.utils import timezone
import os

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class Profile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True)
