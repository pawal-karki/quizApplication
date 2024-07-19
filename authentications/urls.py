from django.contrib import admin
from django.urls import path
from dj_rest_auth.registration.views import RegisterView , VerifyEmailView , ResendEmailVerificationView
from dj_rest_auth.views import LoginView 

urlpatterns = [
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('login/',LoginView.as_view(), name='rest_login'),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('resend-email/', ResendEmailVerificationView.as_view(), name='rest_resend_email'),
]
