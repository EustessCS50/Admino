import io
import json

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone

from .forms import RegisterForm, ArticleForm, ProfileForm, UserForm
from .models import *

# Import Pagination stuff

from django.core.paginator import Paginator


# Create your views here.


def homePage(request):
    articles = Article.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')[:]
    p = Paginator(articles, 2)
    page = request.GET.get('page')
    pagi_articles = p.get_page(page)

    context = {'articles': articles, 'pagi_articles': pagi_articles}
    return render(request, 'index.html', context)


def homeArtDetail(request, pk):
    article = Article.objects.get(id=pk)
    context = {'article': article}
    return render(request, 'home_arti_detail.html', context)


@login_required(login_url='login')
def dashboardPage(request):
    articles = Article.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')[:10]
    context = {'articles': articles}
    return render(request, 'dashboard.html', context)


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
            return redirect('index')
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
    articles = Article.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')[:]
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


@login_required(login_url='login')
def addArticlePage(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'addarticle.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteArticle(request, pk):
    article = Article.objects.get(id=pk)
    if request:
        article.delete()
    return redirect('articles')


@login_required(login_url='login')
def withdrawPage(request):
    global amount
    if request.user.is_authenticated:
        amount = 0
        profile = request.user.profile
        if request.method == "POST":
            amount = request.POST.get('amount')
            # email = request.user.email
            minimum = 100
            balance = profile.balance
            if balance > minimum and int(amount) >= minimum:
                pass
            else:
                return redirect('withdraw')

    context = {'amount': float(amount)}
    return render(request, 'withdraw.html', context)


def paymentComplete(request):
    body = json.loads(request.body)
    email = request.user.email
    print(f"Response : {body} : User: {email}")
    profile = request.user.profile
    amount = body['amount']
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

    return JsonResponse("Payment Complete Thank You! ", safe=False)


def buyArticle(request, pk):
    if request.user.is_authenticated:
        article = Article.objects.get(id=pk)

    context = {'amount': float(15), 'article': article}
    return render(request, 'buy_article.html', context)


def downloadArticle(request, pk):
    article = Article.objects.get(id=pk)

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    text = c.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont("Helvetica", 14)

    lines = [
        "ADMINO ARTICLES",
        " ",
        " ",
        f"{article.title}",
        "-------------------------- ",
        f"{article.content}",
        " ",
        f"{article.publisher}",
        f"{article.publish_date}"
    ]

    "==================================================================="

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename=f"{article.title}.pdf")


def purchaseComplete(request):
    global message
    body = json.loads(request.body)
    email = request.user.email

    print(f"Response : {body} : User: {email}")

    profile = request.user.profile
    amount = body['amount']
    message = body['message']
    minimum = 100
    balance = profile.balance

    profile.balance -= int(amount)
    profile.save()
    # template = render_to_string(
    #     'mails/withdraw_email_template.html',
    #     {
    #         'name': request.user.username,
    #         'amount': amount,
    #         'balance': profile.balance,
    #     })
    #
    # mail = EmailMessage(
    #     'Admino Withdrawal',
    #     template,
    #     settings.EMAIL_HOST_USER,
    #     [email],
    # )
    # mail.fail_silently = False
    # mail.send()
    if message == "Transaction Complete":
        return redirect('home')

    return JsonResponse("Purchase Complete", safe=False)


def downloadPage(request, pk):
    pass
#     article = Article.objects.get(id=pk)
#     context = {'article': article}
#     return render(request, 'download_page.html', context)
