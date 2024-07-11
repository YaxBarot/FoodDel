from django.urls import path

from .views import Login, Logout, Registration

urlpatterns = [

     path("logout/", Logout.as_view()),
     path("login/", Login.as_view()),
     path("registration/", Registration.as_view())
]
