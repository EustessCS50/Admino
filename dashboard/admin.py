from django.contrib import admin
from .models import Account, Article, Profile

# Register your models here.

admin.site.register(Article)
admin.site.register(Account)
admin.site.register(Profile)