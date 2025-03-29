from django.urls import path
from .views import RegistrationView, CustomLoginView, VerifyEmailView, PasswordResetRequestView, PasswordResetConfirmView, ResendConfirmationEmailView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('resend-confirmation-email/', ResendConfirmationEmailView.as_view(), name='resend-confirmation-email'),
]