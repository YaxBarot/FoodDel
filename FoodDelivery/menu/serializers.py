from rest_framework import serializers
from .models import MenuCategory, MenuItem


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"

class RestaurantMenuSerializer(serializers.ModelSerializer):
    category = MenuCategorySerializer(read_only=True, source='category_id')
    class Meta:
        model = MenuItem
        fields = ["restaurant_id","menu_id","name","description","price","item_pic","category"]

class MenuItemavailablitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["is_deleted"]


