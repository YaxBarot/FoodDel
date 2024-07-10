from rest_framework import serializers

from .models import  AdministratorAuthTokens, RestaurantAuthTokens, CustomerAuthTokens


class CustomerAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAuthTokens
        fields = "__all__"

class RestaurantAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantAuthTokens
        fields = "__all__"

class AdministratorAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministratorAuthTokens
        fields = "__all__"