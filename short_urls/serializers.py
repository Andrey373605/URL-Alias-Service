from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import ShortURL, Click
from .services import create_short_url
from . import constants


class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = [
            'id',
            'original_url',
            'short_key',
            'created_at',
            'expires_at',
            'is_active',
        ]
        read_only_fields = ['id', 'short_key', 'created_at']


class ShortURLStatsSerializer(serializers.ModelSerializer):
    last_hour_clicks = serializers.IntegerField()
    last_day_clicks = serializers.IntegerField()
    all_time_clicks = serializers.IntegerField()

    class Meta:
        model = ShortURL
        fields = [
            'original_url',
            'short_key',
            'last_hour_clicks',
            'last_day_clicks',
            'all_time_clicks',
        ]
        read_only_fields = fields


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ['clicked_at']
        read_only_fields = ['clicked_at']


class CreateShortURLSerializer(serializers.Serializer):
    original_url = serializers.URLField(max_length=constants.MAX_URL_LENGTH)
    expires_days = serializers.IntegerField(
        min_value=constants.SHORT_URL_MIN_EXPIRE_DAYS,
        max_value=constants.SHORT_URL_MAX_EXPIRE_DAYS,
        default=constants.SHORT_URL_DEFAULT_EXPIRE_DAYS
    )
    custom_key = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[
            RegexValidator(
                regex=constants.SHORT_KEY_REGEX,
                message=f"Key can only contain: {constants.SHORT_KEY_ALPHABET}",
                code="invalid_key_format"
            )
        ]
    )

    def validate_custom_key(self, value):
        if not value:
            return value
        
        if ShortURL.objects.filter(short_key=value).exists():
            raise serializers.ValidationError(
                "This custom key is already in use"
            )
        return value

    def create(self, validated_data):
        return create_short_url(
            original_url=validated_data['original_url'],
            expires_days=validated_data.get('expires_days'),
            custom_key=validated_data.get('custom_key')
        )


class DeactivateResponseSerializer(serializers.Serializer):
    status = serializers.CharField()