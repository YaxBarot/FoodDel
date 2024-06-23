from django.db import models

from FoodDel.FoodDelivery.restaurant.models import RestaurantProfile


class MenuCategory(models.Model):
    class Meta:
        db_table = 'fd_menu_category'
    name = models.CharField(max_length=100)
    category_id = models.BigAutoField(primary_key=True)


class MenuItem(models.Model):
    class Meta:
        db_table = 'fd_menu_item'
    restaurant_id = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)
    category_id = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
