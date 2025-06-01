from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError as DRFValidationError
from ..models import ShortURL

class DeactivateShortURLService:
    """
    Service for deactivating short URL
    """

    @classmethod
    def execute(cls, short_key: str) -> ShortURL:
        short_url = get_object_or_404(ShortURL, short_key=short_key)

        if not short_url.is_active:
            raise DRFValidationError("URL already deactivated")

        with transaction.atomic():
            short_url.is_active = False
            short_url.save()

        return short_url
