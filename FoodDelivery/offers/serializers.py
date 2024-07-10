from rest_framework import serializers
from .models import Offers


class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = ["offer_id", "item_id", "discount", "item_quantity", "free_item", "free_item_quantity", "type"]

class OffersApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = ["is_approved"]