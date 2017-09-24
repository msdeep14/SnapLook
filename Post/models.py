from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Album(models.Model):
    user = models.ForeignKey(User,)
    image_url = models.CharField(max_length = 200)
    date = models.DateTimeField(default = timezone.now())
    retweets = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username
