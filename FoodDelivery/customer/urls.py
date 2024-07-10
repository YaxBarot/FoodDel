from django.urls import path

from .cart import AddToCart, ApplyOffer, Cartcheckout, DeleteInCart, GetCart

from .homepage import ShowRestaurantList

from .views import Registration, Login, Logout, OTPVerification, ResetPassword, ForgotPassword,GetRestaurantMenu

from .ratings import RateRestaurant


urlpatterns = [
    path("register/", Registration.as_view()),
    path("login/", Login.as_view()),
    path("otp_verification/", OTPVerification.as_view()),
    path("reset_password/", ResetPassword.as_view()),
    path("forgot_password/", ForgotPassword.as_view()),
    path("logout/", Logout.as_view()),
    path("showrestaurantlist/", ShowRestaurantList.as_view()),
    path("getrestaurantmenu/", GetRestaurantMenu.as_view()),
    path("addtocart/", AddToCart.as_view()),
    path('deleteincart/<int:cart_id>/', DeleteInCart.as_view()),
    path("getcart/", GetCart.as_view()),
    path("cartcheckout/", Cartcheckout.as_view()),
    path("raterestaurant/",RateRestaurant.as_view()),
    path("applyoffer/<int:restaurant_id>/",ApplyOffer.as_view())
 
]
