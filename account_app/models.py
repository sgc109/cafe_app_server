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
    comment = models.CharField(max_length=100, blank=True)

    def alias_user(self):
        return self.user.id
