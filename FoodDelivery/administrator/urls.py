from django.urls import path

from .views import Login, Logout, Registration

urlpatterns = [

     path("logout/", Logout.as_view())

 
]
