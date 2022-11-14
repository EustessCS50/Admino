from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Article, Profile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2'}


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = {'pic',}

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
