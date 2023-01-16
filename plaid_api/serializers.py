from rest_framework import serializers
from .models import UserToken


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ("id", "link_token", "token_status", "user_id")
