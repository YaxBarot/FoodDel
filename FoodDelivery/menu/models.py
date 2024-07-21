from django.db import models

from common.models import Audit
from restaurant.models import RestaurantProfile

class MenuCategory(Audit):
    class Meta:
        db_table = 'fd_menu_category'
    name = models.CharField(max_length=100)
    category_id = models.BigAutoField(primary_key=True)


class MenuItem(Audit):
    class Meta:
        db_table = 'fd_menu_item'
    restaurant_id = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)
    category_id = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    menu_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_pic = models.ImageField(upload_to='Images/ItemPic', db_column="item_pic", null=True, blank=True)

