from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from ..models import ShortURL
from .short_key_generator import ShortKeyGenerator
from ..constants import SHORT_URL_DEFAULT_EXPIRE_DAYS

class CreateShortURLService:
    """
    Service for creating a short link
    """

    @classmethod
    def execute(cls, original_url: str, custom_key: str = None, expires_days: int = None) -> ShortURL:
        if not original_url:
            raise ValueError("Original URL is required")

        if custom_key:
            short_key = custom_key
        else:
            short_key = ShortKeyGenerator.generate()

        expire_days = expires_days or SHORT_URL_DEFAULT_EXPIRE_DAYS
        expiration = timezone.now() + timezone.timedelta(days=expire_days)

        with transaction.atomic():
            short_url_obj = ShortURL(
                original_url=original_url,
                short_key=short_key,
                expires_at=expiration,
                is_active=True
            )
            short_url_obj.full_clean() 
            short_url_obj.save()

        return short_url_obj
