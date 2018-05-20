from django.db import models
from django.utils import timezone
from account_app.models import Profile

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class Post(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
