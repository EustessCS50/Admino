from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.homePage, name='index'),
    path('articles/<str:pk>/', views.homeArtDetail, name='home_article'),
    path('dashboard/', views.dashboardPage, name='home'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('profile/', views.profilePage, name='profile'),
    path('account/withdrawal', views.withdrawPage, name='withdraw'),
    path('account/withdrawal/complete', views.paymentComplete, name='complete'),
    path('user/articles/', views.articlePage, name='articles'),
    path('user/articles/add', views.addArticlePage, name='add_article'),
    path('user/articles/<str:pk>/', views.articleDetailPage, name='article'),
    path('user/articles/<str:pk>/edit', views.editArticlePage, name='edit_article'),
    path('user/articles/<str:pk>/delete', views.deleteArticle, name='delete_article'),
]

# Password Reset

urlpatterns += [
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="mails/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="mails/password_reset_sent.html"),
         name='password_reset_done'),
    path('reset<uidb64><token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="mails/password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="mails/password_reset_done.html"),
         name='password_reset_complete'),
]