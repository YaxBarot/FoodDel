from django.urls import path
from .views import MenuCategoryCreate

urlpatterns = [
    path('create-category/', MenuCategoryCreate.as_view())
]
