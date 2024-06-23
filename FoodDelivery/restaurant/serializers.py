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
