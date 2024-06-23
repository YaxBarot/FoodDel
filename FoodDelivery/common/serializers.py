from rest_framework import serializers

from .models import  RestaurantAuthTokens, CustomerAuthTokens


class CustomerAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAuthTokens
        fields = "__all__"

class RestaurantAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantAuthTokens
        fields = "__all__"