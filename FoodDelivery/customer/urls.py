from django.urls import path

from .views import Registration, Login, Logout, OTPVerification, ResetPassword, ForgotPassword


urlpatterns = [
    path("register/", Registration.as_view()),
    path("login/", Login.as_view()),
    path("otp_verification/", OTPVerification.as_view()),
    path("reset_password/", ResetPassword.as_view()),
    path("forgot_password/", ForgotPassword.as_view()),
    path("logout/", Logout.as_view()),
]
