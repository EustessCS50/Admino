from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='profile_pics')

    def __str__(self):
        return self.user.username


class Article(models.Model):
    title = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    content = models.TextField(max_length=500, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Account(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=10)
