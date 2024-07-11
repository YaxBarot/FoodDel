from enum import Enum
from django.db import models
from restaurant.models import RestaurantProfile
from menu.models import MenuItem
from common.models import Audit


class OfferType(Enum):
    ON_CART = "on_cart"
    ON_ITEM = "on_item"
    
    @classmethod
    def choices(cls):
        return [(type.name, type.value) for type in cls]
    

class Offers(Audit):
    class Meta:
        db_table = "fd_offers"
    offer_id = models.BigAutoField(primary_key=True)
    item_id = models.ForeignKey(MenuItem,  related_name='item_id',on_delete=models.CASCADE,null=True)
    discount = models.IntegerField(default=0)
    item_quantity = models.IntegerField(null=True)
    free_item = models.ForeignKey(MenuItem, related_name='free_item_id', on_delete=models.CASCADE,null=True)
    free_item_quantity = models.IntegerField(null=True)
    type = models.CharField(choices=OfferType.choices(), max_length=255,
                                       default=OfferType.ON_CART.name)
    is_approved = models.BooleanField(default=0)
    restaurant_id = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)
    allow_multiple_offers = models.BooleanField(default=0)


