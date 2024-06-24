
from rest_framework import serializers
from .models import Customers, CustomerOTP
from restaurant.models import RestaurantProfile

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = "__all__"
        
class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ["password"]

class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOTP
        fields = ["customer_id","otp"]

class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantProfile
        fields = ["restaurant_id","restaurant_name","Restaurant_type","address"]