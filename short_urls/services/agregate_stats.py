from django.utils import timezone
from django.db.models import Q, Count, QuerySet
from rest_framework.exceptions import NotFound
from ..models import ShortURL


class ShortURLStatsService:
    """
    Service for obtaining statistics on short URLs.
    """

    @staticmethod
    def _annotate_stats(queryset: QuerySet) -> QuerySet:
        now = timezone.now()
        hour_ago = now - timezone.timedelta(hours=1)
        day_ago = now - timezone.timedelta(days=1)

        return queryset.annotate(
            last_hour_clicks=Count(
                'clicks',
                filter=Q(clicks__clicked_at__gt=hour_ago)
            ),
            last_day_clicks=Count(
                'clicks',
                filter=Q(clicks__clicked_at__gt=day_ago)
            ),
            all_time_clicks=Count('clicks')
        )

    @staticmethod
    def _format_stats(obj: ShortURL) -> dict:
        return {
            'short_key': obj.short_key,
            'original_url': obj.original_url,
            'last_hour_clicks': obj.last_hour_clicks,
            'last_day_clicks': obj.last_day_clicks,
            'all_time_clicks': obj.all_time_clicks
        }

    @classmethod
    def list_all_stats(cls) -> list[dict]:
        queryset = cls._annotate_stats(ShortURL.objects.all()).order_by('-all_time_clicks')
        return [cls._format_stats(obj) for obj in queryset]

    @classmethod
    def detail_stats(cls, short_key: str) -> dict:
        try:
            obj = cls._annotate_stats(
                ShortURL.objects.filter(short_key=short_key)
            ).get()
        except ShortURL.DoesNotExist:
            raise NotFound("ShortURL not found")

        return cls._format_stats(obj)
