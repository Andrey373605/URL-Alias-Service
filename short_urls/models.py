from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import URLValidator
from . import constants



class ShortURL(models.Model):
    """Model representing a shortened URL."""
    original_url = models.URLField(
        max_length=constants.MAX_URL_LENGTH,
        validators=[URLValidator()],
        help_text="Original long URL to be shortened"
    )
    short_key = models.CharField(
        max_length=constants.SHORT_KEY_MAX_LENGTH,
        unique=True,
        db_index=True,
        help_text="Unique key for the shortened URL"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the URL was shortened"
    )
    expires_at = models.DateTimeField(
        help_text="Expiration timestamp for the shortened URL"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Flag indicating if the URL is active"
    )
    

    @property
    def click_count(self):
        """Return the number of clicks for this short URL."""
        return self.clicks.count()
    
    def is_expired(self):
        """Check if the short URL has expired."""
        return timezone.now() > self.expires_at
        
    def clean(self):
        """Additional model-wide validation."""
        super().clean()
        
        if self.expires_at <= timezone.now():
            raise ValidationError("Expiration date must be in the future")
        
    def save(self, *args, **kwargs):
        """Save model with full validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_key} → {self.original_url}"


class Click(models.Model):
    """Model tracking clicks on short URLs."""
    short_url = models.ForeignKey(
        ShortURL,
        on_delete=models.CASCADE,
        related_name='clicks',
        help_text="Associated shortened URL"
    )
    clicked_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the click occurred"
    )

    class Meta:
        indexes = [
            models.Index(fields=['-clicked_at']),
        ]
        ordering = ['-clicked_at']
        verbose_name = "URL Click"
        verbose_name_plural = "URL Clicks"

    def __str__(self):
        return f"Click on {self.short_url} at {self.clicked_at}"