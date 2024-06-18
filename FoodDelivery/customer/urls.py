from django.urls import path

from .views import Registration, Test


urlpatterns = [
    path("register/", Registration.as_view()),
    path("test/",Test.as_view())
]
