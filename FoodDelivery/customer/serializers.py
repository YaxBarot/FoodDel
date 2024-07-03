
from rest_framework import serializers
from .models import Cart, Customers, CustomerOTP
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

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id" , "menu_item" , "total_price"]

class ShowCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart 
        fields = "__all__"
    
class JSONMenuSerializer(serializers.Serializer):
    restaurant_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    menu_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500, allow_blank=True, allow_null=True)
    price = serializers.CharField(max_length=100)
    quantity     = serializers.IntegerField()