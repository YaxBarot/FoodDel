from django.db import models

from restaurant.models import RestaurantProfile
from menu.models import MenuItem
from common.models import Audit
from offers.models import Offers

class Customers(Audit):
    class Meta:
        db_table = 'fd_customers'

    id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=255)

    email = models.EmailField(unique=True)
    password = models.TextField()

    mobile_no = models.CharField(max_length=50, null=True, unique=True, db_column="mobile_number")

    dob = models.DateField(db_column="usr_dob", null=True)
    credit = models.CharField(max_length=255,default="1000")


class CustomerOTP(Audit):
    class Meta:
        db_table = "fd_customer_otp"

    customer_otp_id = models.BigAutoField(primary_key=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    otp = models.CharField(max_length=255)

class Cart(Audit):
    class Meta:
        db_table = "fd_cart"
    customer_cart_id = models.BigAutoField(primary_key=True)

    restaurant_id = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)
    id = models.ForeignKey(Customers, on_delete=models.CASCADE)

    menu_item = models.JSONField()

    total_price = models.CharField(max_length=255,default=0)

    is_ordered = models.BooleanField(default=0)
    is_offer_applied = models.BooleanField(default=0)


class OffersHistory(Audit):
    class Meta:
        db_table = "fd_offers_history"

    offers_history_id = models.BigAutoField(primary_key=True)

    offers_id = models.ForeignKey(Offers, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)




class RatingHistory(Audit):
    class Meta:
        db_table = "fd_rating_history"

    rating_id = models.BigAutoField(primary_key=True)

    restaurant_id = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    rating = models.IntegerField()

