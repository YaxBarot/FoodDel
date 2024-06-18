from rest_framework import serializers

from .models import AuthTokens


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthTokens
        fields = "__all__"
