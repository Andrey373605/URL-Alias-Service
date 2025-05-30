import secrets
from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.contrib.auth.models import User
from . import constants


def get_default_expiration():
    return timezone.now() + timezone.timedelta(days=constants.SHORT_URL_DEFAULT_EXPIRE_DAYS)


class ShortURL(models.Model):
    original_url = models.URLField(max_length=constants.MAX_URL_LENGTH, validators=[URLValidator()])
    short_key = models.CharField(max_length=constants.SHORT_KEY_MAX_LENGTH, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_default_expiration)
    is_active = models.BooleanField(default=True)
    click_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def save(self, *args, **kwargs):
        from .services import generate_short_key
        if not self.short_key:
            self.short_key = generate_short_key()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.short_key} -> {self.original_url}"
    

class Click(models.Model):
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_url} click at {self.clicked_at}"

    class Meta:
        indexes = [
            models.Index(fields=['-clicked_at']),
        ]
        ordering = ['-clicked_at']
    

