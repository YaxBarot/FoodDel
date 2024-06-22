import datetime
from django.db import models
from common.models import Audit

class RestaurantProfile(Audit):
    class Meta:
        db_table = "fd_restaurant_profile"

    restaurant_id = models.BigAutoField(primary_key=True)
    # restaurant_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # address = models.CharField(max_length=255)
    # restaurant_product_review_average = models.CharField(max_length=255)

class RestaurantOTP(Audit):
    class Meta:
        db_table = "fd_restaurant_otp"

    restaurant_otp_id = models.BigAutoField(primary_key=True)
    restaurant_id = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)
    otp = models.CharField(max_length=255)
