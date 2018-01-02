from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Album(models.Model):
    user = models.ForeignKey(User,)
    image_url = models.CharField(max_length = 200)
    date = models.DateTimeField(default = timezone.now())
    retweet_count = models.IntegerField(default = 0)
    like_count = models.IntegerField(default = 0)
    emotion = models.CharField(max_length = 50, default = 'happiness')
    hashtag = models.CharField(max_length = 200, default = '#katrinakaif')

    def __str__(self):
        return self.user.username
