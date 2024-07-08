from django.urls import path
from .views import CartApproval, ForgotPassword, GetRestaurantType, OTPVerification, OperationalStatus, Registration,Logout, Login, ResetPassword


app_name = "Restaurant"

urlpatterns = [
    
    path("getrestauranttype/", GetRestaurantType.as_view()),
    path("registration/", Registration.as_view()),
    path("login/", Login.as_view()),
    path("otpverification/", OTPVerification.as_view()),
    path("resetpassword/", ResetPassword.as_view()),
    path("forgotpassword/", ForgotPassword.as_view()),
    path("logout/", Logout.as_view()),
    path("cartapproval/", CartApproval.as_view()),
    path("operationalstatus/", OperationalStatus.as_view())
    
]