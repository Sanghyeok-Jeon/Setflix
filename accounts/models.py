from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

# Create your models here.

class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')
    is_staff = models.BooleanField(default=False)

def user_path(instance, filename):
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extenstion = filename.split('.')[-1]
    
    return '%s%s%s' % (instance.owner.username, pid, extenstion)

class Photo(models.Model):
    image = models.ImageField(upload_to=user_path)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbnail_image = models.ImageField(blank=True)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=40, blank=True)
    introduction = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    image_thumbnail = ImageSpecField(
                        source='image', 
                        processors=[ResizeToFit(300, 300)],
                        format='JPEG',
                        options={'quality': 60}
                        )

