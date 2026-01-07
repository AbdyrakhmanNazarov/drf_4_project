from django.urls import path
from accounts.views import (
    RegisterView,
    LoginView,
    ProfileView,
    ChangePasswordView,
    LogoutView,
    DeactivateAccountView,
    RequestPasswordResetView,
    VerifyPasswordResetOTPView,
    ResetPasswordView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('deactivate/', DeactivateAccountView.as_view(), name='deactivate'),
    path('password-reset/request/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('password-reset/verify/', VerifyPasswordResetOTPView.as_view(), name='verify-password-reset'),
    path('password-reset/complete/', ResetPasswordView.as_view(), name='complete-password-reset'),
]
