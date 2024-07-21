from customer.models import Cart
from rest_framework import serializers

from .models import RestaurantOTP, RestaurantProfile, RestaurantOTP





class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantProfile
        fields = "__all__"

class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantProfile
        fields = ["password"]

class OTPVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantOTP
        fields = ["restaurant_id","otp"]

class OperationalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantProfile
        fields = ["operational_status"]

class CartItemSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField()
    id = serializers.IntegerField()
    menu_item = serializers.JSONField()
    total_price = serializers.CharField(max_length=255)
    is_ordered = serializers.BooleanField() 
