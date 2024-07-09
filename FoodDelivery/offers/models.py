from django.db import models
from menu.models import MenuItem
from common.models import Audit

class Offers(Audit):
    class Meta:
        db_table = "fd_offers"
    offer_id = models.BigAutoField(primary_key=True)
    item_id = models.ForeignKey(MenuItem,  related_name='item_id',on_delete=models.CASCADE)
    discount = models.IntegerField()
    item_quantity = models.IntegerField()
    free_item = models.ForeignKey(MenuItem, related_name='free_item_id', on_delete=models.CASCADE)
    free_item_quantity = models.IntegerField()