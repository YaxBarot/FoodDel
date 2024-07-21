from enum import Enum
from django.db import models
from common.models import Audit


class RestaurantType(Enum):
    ALL_TYPES = "All types"
    RESTRAUNT = "Restraunt"
    FAST_FOOD = "Fast Food"
    FAST_CASUAL = "Fast Casual"
    CASUAL_DINING = "Casual Dining"
    FINE_DINING = "Fine Dining"
    CAFE = "Café or Bistro"
    BUFFET = "Buffet"
    FOOD_TRUCK = "Food Truck"
    FAMILY_STYLE = "Family Style"
    POP_UP = "Pop-up Restaurant"
    ETHNIC = "Ethnic Restaurant"
    BRASSERIE = "Brasserie"
    PIZZERIA = "Pizzeria"
    STEAKHOUSE = "Steakhouse"
    SEAFOOD = "Seafood Restaurant"
    VEGETARIAN_VEGAN = "Vegetarian/Vegan Restaurant"

    @classmethod
    def choices(cls):
        return [(type.name, type.value) for type in cls]


class RestaurantProfile(Audit):
    class Meta:
        db_table = "fd_restaurant_profile"

    restaurant_id = models.BigAutoField(primary_key=True)

    restaurant_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    Restaurant_type = models.CharField(choices=RestaurantType.choices(), max_length=255,
                                       default=RestaurantType.RESTRAUNT.name)
    credit = models.CharField(max_length=255, default="0")
    email = models.EmailField(unique=True)

    operational_status = models.BooleanField(default=0)

    rating = models.FloatField(default=0.0)
    no_of_ratings = models.IntegerField(default=0)

    Restaurant_pic = models.ImageField(upload_to='Images/RestaurantPic',default="Screenshot 2024-07-12 214916.png", db_column="restaurant_pic", null=True, blank=True)

class RestaurantOTP(Audit):
    class Meta:
        db_table = "fd_restaurant_otp"

    restaurant_otp_id = models.BigAutoField(primary_key=True)

    restaurant_id = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)

    otp = models.CharField(max_length=255)
