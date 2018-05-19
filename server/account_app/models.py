from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User

#class User(models.Model):
#    id = models.CharField(max_length=20, primary_key=True, blank=True)
#    pw = models.CharField(max_length=20)

class Profile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
#
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()
