from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User

#class User(models.Model):
#    id = models.CharField(max_length=20, primary_key=True, blank=True)
#    pw = models.CharField(max_length=20)

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)
    
class Profile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
