from django.db import models
from django.utils import timezone
from account_app.models import Profile
from datetime import date
import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(date.today().strftime('photos/%Y/%m/%d/'), filename)

class Post(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)
    # published_date = models.DateTimeField(blank=True, null=True)

    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()

    # def __str__(self):
    #     return self.title
