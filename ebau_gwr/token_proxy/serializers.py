from rest_framework.exceptions import ValidationError
from rest_framework_json_api import serializers

from . import models
from .client import HousingStatClient


class TokenProxySerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        client = HousingStatClient()
        token_resp = client.get_token(username=obj.username, password=obj.password)
        if token_resp["success"] is True:
            return token_resp["token"]
        raise ValidationError(
            {
                token_resp["status_code"]: {
                    "source": "external",
                    "reason": token_resp["reason"],
                }
            }
        )

    def create(self, validated_data):
        user = self.context["request"].user

        username = validated_data.get("username")
        password = validated_data.get("password")

        if username and password:
            user_creds, _ = models.HousingStatCreds.objects.update_or_create(
                owner=user.username,
                defaults={"username": username, "password": password},
            )
        else:
            user_creds = models.HousingStatCreds.objects.filter(owner=user.username)
            user_creds.update(**validated_data)
            user_creds = user_creds.first()
            if not user_creds:
                raise ValidationError(
                    {
                        400: {
                            "source": "internal",
                            "reason": f'No housing stat credentials found for user "{user.username}"',
                        }
                    }
                )

        return user_creds

    class Meta:
        model = models.HousingStatCreds
        fields = (
            "username",
            "password",
            "token",
        )
