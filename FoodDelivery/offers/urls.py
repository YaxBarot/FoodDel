from django.urls import path

from .views import OffersCreate, OffersDelete

urlpatterns = [
    path("create_offers/", OffersCreate.as_view()),
    path('delete_offers/<int:offer_id>/', OffersDelete.as_view()),
]
