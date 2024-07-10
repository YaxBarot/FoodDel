from django.urls import path

from .views import OffersApproval, OffersCreate, OffersDelete

urlpatterns = [
    path("create_offers/", OffersCreate.as_view()),
    path('delete_offers/<int:offer_id>/', OffersDelete.as_view()),
    path('offer_approval/<int:offer_id>/', OffersApproval.as_view()),
]