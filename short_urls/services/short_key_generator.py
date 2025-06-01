import secrets
from django.core.exceptions import ObjectDoesNotExist
from ..models import ShortURL
from ..constants import SHORT_KEY_ALPHABET, SHORT_KEY_LENGTH, MAX_SHORT_KEY_GENERATION_ATTEMPTS

class ShortKeyGenerator:
    """
    Генератор уникального короткого ключа.
    """

    @staticmethod
    def generate() -> str:
        for _ in range(MAX_SHORT_KEY_GENERATION_ATTEMPTS):
            key = ''.join(secrets.choice(SHORT_KEY_ALPHABET) for _ in range(SHORT_KEY_LENGTH))
            try:
                ShortURL.objects.get(short_key=key)
            except ObjectDoesNotExist:
                return key
        raise RuntimeError("Failed to generate unique key after multiple attempts")