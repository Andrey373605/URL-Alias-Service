from django.urls import path

from .views import ( 
    DeactivateShortURLView,
    ShortURLListCreateView,
    ShortURLRetrieveView,
    ShortURLStatsDetailView,
    ShortURLStatsView
)

urlpatterns = [
    path('short-urls/', ShortURLListCreateView.as_view(), name='create-list'),
    path('short-urls/stats/', ShortURLStatsView.as_view(), name='stats'),
    path('short-urls/<str:short_key>/', ShortURLRetrieveView.as_view(), name='detail'),
    path('short-urls/<str:short_key>/deactivate', DeactivateShortURLView.as_view(), name='deactivate'),
    path('short-urls/stats/<str:short_key>/', ShortURLStatsDetailView.as_view(), name='detail-stats'),
]