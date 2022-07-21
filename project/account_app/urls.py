from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from . import views
from . import apis

urlpatterns = [
    path('test_account', TemplateView.as_view(template_name='account_app/base.py.html'), name='test_account'),
    path('accounts/profile', views.AccountProfileView.as_view(), name='account_profile'),
    path('sign_up', views.SignUpView.as_view(), name='sign_up'),
    path('login', views.AccountLoginView.as_view(), name='login'),
    path('logout', views.AccountLogoutView.as_view(), name='logout'),

    path('password_changed', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('change_password', views.UserChangePasswordView.as_view(), name='user_change_password'),

    path('api/v1/login', apis.LoginApiView.as_view(), name='api_v1_login'),
    path('api/v1/logout', apis.LogoutApiView.as_view(), name='api_v1_logout'),
    path('api/v1/register', apis.RegisterApiView.as_view(), name='api_v1_register'),
    path('api/v1/user', apis.UserDetailApiView.as_view(), name='api_v1_user'),
]
