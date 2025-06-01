from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from ..models import ShortURL, Click

class GoneException(Exception):
    """
    Исключение, означающее, что ссылка найдена, но неактивна или истекла.
    """

    pass

class RedirectShortURLService:
    """
    Сервис для обработки редиректа по короткому ключу.
    """

    @classmethod
    def execute(cls, short_key: str) -> str:
        now = timezone.now()
        try:
            short_url = ShortURL.objects.get(
                short_key=short_key,
                is_active=True,
                expires_at__gt=now
            )
        except ShortURL.DoesNotExist:
            # Если даже неактивная или просроченная запись существует — возвращаем Gone
            if ShortURL.objects.filter(short_key=short_key).exists():
                raise GoneException("URL is inactive or expired")
            raise NotFound("URL does not exist")

        # Фиксируем клик
        Click.objects.create(short_url=short_url)
        return short_url.original_url
