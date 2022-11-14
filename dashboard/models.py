from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='profile_pics', blank=True)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return self.user.username

    def createProfile(sender, **kwargs):
        if kwargs['created']:
            profile = Profile.objects.created(user=kwargs['instance'])

    post_save.connect(createProfile, sender=User)


class Article(models.Model):
    title = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    content = models.TextField(max_length=500, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


