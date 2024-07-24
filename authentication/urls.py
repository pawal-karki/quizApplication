from django.contrib import admin
from django.urls import include, path

from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ResendEmailVerificationView
from dj_rest_auth.views import LoginView
from .views import email_confirm_redirect,password_reset_confirm_redirect
from dj_rest_auth.views import PasswordChangeView, PasswordResetConfirmView,PasswordResetView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('resend-email/', ResendEmailVerificationView.as_view(),name="rest_resend_email"),
    path('account-confirm-email/<str:key>',email_confirm_redirect, name='account_confirm_email'),
    path('account-email-verification-sent/', VerifyEmailView.as_view(),name='account_email_verification_sent'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path("password/reset/redirect/<str:userId>/<str:token>", password_reset_confirm_redirect, name="password_reset_confirm")
]
