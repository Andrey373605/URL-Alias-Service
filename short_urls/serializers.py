from cmath import exp
from rest_framework import serializers
from .models import ShortURL, Click
from .services import create_short_url
from . import constants

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['id', 'original_url', 'short_key', 'created_at', 
                 'expires_at', 'is_active', 'click_count', 'user']
        read_only_fields = ['id', 'short_key', 'created_at', 'click_count', 'user']


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['clicked_at']
        read_only_fields = ['clicked_at']


class CreateShortURLSerializer(serializers.Serializer):
    original_url = serializers.URLField(max_length=2048)

    expires_days = serializers.IntegerField(
        min_value=constants.SHORT_URL_MIN_EXPIRE_DAYS,
        max_value=constants.SHORT_URL_MAX_EXPIRE_DAYS,
        default=constants.SHORT_URL_DEFAULT_EXPIRE_DAYS
    )

    custom_key = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True
    )

    def create(self, validated_data):
        return create_short_url(
            original_url=validated_data['original_url'],
            user=self.context['request'].user,
            expires_days=validated_data['expires_days'],
            custom_key=validated_data['custom_key']
        )
    

class TopURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['short_key', 'original_url', 'click_count']
