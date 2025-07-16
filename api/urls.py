from django.urls import path
from .views import ShortURLCreate, ShortURLStats, redirect_short_url

urlpatterns = [
    path('shorturls', ShortURLCreate.as_view(), name='create_short_url'),
    path('shorturls/<str:shortcode>', ShortURLStats.as_view(), name='short_url_stats'),
    path('<str:shortcode>', redirect_short_url, name='redirect_short_url'),
]
