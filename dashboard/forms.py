from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Article


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2'}


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
