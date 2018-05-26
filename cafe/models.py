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
    type = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    # birth = models.DateTimeField()
    comment = models.CharField(max_length=100, blank=True)

    def alias_user(self):
        return self.user.id

class Category(models.Model):
    name = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=50, blank=True)
    state = models.IntegerField(default=0)
    taking_time = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __str__(self):
        return 'order ' + '{}'.format(self.id)

class Menu(models.Model):
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    name = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    taking_time = models.IntegerField(default=0)

    def __str__(self):
        return 'menu ' + '{}'.format(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cnt = models.PositiveIntegerField()

    def __str__(self):
        return 'item ' + '{}'.format(self.id)

class WaitingTime(models.Model):
    value = models.PositiveIntegerField()

    def __str__(self):
        return '{}'.format(self.value)
