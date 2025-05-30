from .models import ShortURL
from django.utils import timezone
from . import constants
import secrets


def create_short_url(original_url, user=None, custom_key=None, expires_days=1):
    if custom_key:
        if ShortURL.objects.filter(short_key=custom_key).exists():
            raise ValueError("Custom key already exists")
        short_key = custom_key
    else:
        short_key = generate_short_key()
    
    expires_at = timezone.now() + timezone.timedelta(days=expires_days)
    
    return ShortURL.objects.create(
        original_url=original_url,
        short_key=short_key,
        expires_at=expires_at,
        user=user
    )

def generate_short_key(length=constants.SHORT_KEY_LENGTH):
    key = secrets.token_urlsafe(constants.TOKEN_BYTES)[:length]
    while ShortURL.objects.filter(short_key=key).exists():
        key = secrets.token_urlsafe(constants.TOKEN_BYTES)[:length]
    return key