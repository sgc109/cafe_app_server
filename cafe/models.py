from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os
import uuid
from datetime import date

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(date.today().strftime('photos/%Y/%m/%d/'), filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    user_type = models.IntegerField()
    point = models.IntegerField()
    birth = models.DateTimeField()
    comment = models.CharField(max_length=100, blank=True)

    def alias_user(self):
        return self.user.id

class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=50, blank=True)
    state = models.IntegerField()
    taking_time = models.IntegerField()
    price = models.IntegerField()

class Category(models.Model):
    name = models.CharField(max_length=20, blank=True)

class Menu(models.Model):
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.IntegerField()
    name = models.CharField(max_length=20, blank=True)
