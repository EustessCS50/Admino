from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .forms import RegisterForm, ArticleForm
from .models import *


# Create your views here.

@login_required(login_url='login')
def homePage(request):
    articles = Article.objects.all()
    profiles = Profile.objects.all()
    context = {'articles': articles, 'profiles': profiles}
    return render(request, 'index.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            print(f'{username}: {password}: {email}')
            form.save()
            if form.save():
                template = render_to_string('mails/email_template.html', {'name': username})

                mail = EmailMessage(
                    'Admino Account',
                    template,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                mail.fail_silently = False
                mail.send()

                return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)


def loginPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password incorrect! ")
            return redirect('login')

    context = {'form': form}
    return render(request, 'login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profilePage(request):
    context = {}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def articlePage(request, pk):
    form = ArticleForm()
    article = Article.objects.get(id=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'article': article, 'form': form}
    return render(request, 'article.html', context)
