from rest_framework import serializers
from .models import Customers

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = "__all__"
