from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone

from .forms import RegisterForm, ArticleForm, ProfileForm, UserForm
from .models import *


# Create your views here.

@login_required(login_url='login')
def homePage(request):
    articles = Article.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')[:10]
    context = {'articles': articles}
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
    profile = request.user
    if request.method == "POST":
        form = UserForm(request.POST, instance=profile)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('home')
    else:
        form = UserForm(instance=profile)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def articlePage(request):
    form = ArticleForm()
    articles = Article.objects.all()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'articles': articles, 'form': form}
    return render(request, 'articles.html', context)


@login_required(login_url='login')
def articleDetailPage(request, pk):
    form = ArticleForm()
    article = Article.objects.get(id=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'article': article, 'form': form}
    return render(request, 'article_detail.html', context)


def addArticlePage(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'addarticle.html', context)


def editArticlePage(request, pk):
    article = Article.objects.get(id=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article', article.id)
    else:
        form = ArticleForm(instance=article)

    context = {'form': form, 'article': article}
    return render(request, 'editarticle.html', context)


def deleteArticle(request, pk):
    article = Article.objects.get(id=pk)
    if request:
        article.delete()
    return redirect('articles')


def withdrawPage(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        if request.method == "POST":
            amount = request.POST.get('amount')
            email = request.user.email
            minimum = 100
            balance = profile.balance
            if balance > minimum and int(amount) >= minimum:
                profile.balance -= int(amount)
                profile.save()
                template = render_to_string(
                    'mails/withdraw_email_template.html',
                    {
                        'name': request.user.username,
                        'amount': amount,
                        'balance': profile.balance,
                    })

                mail = EmailMessage(
                    'Admino Withdrawal',
                    template,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                mail.fail_silently = False
                mail.send()

                return redirect('home')
            else:
                return redirect('withdraw')

    context = {}
    return render(request, 'withdraw.html', context)
