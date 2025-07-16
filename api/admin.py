from django.contrib import admin
from .models import ShortURL, Click

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('id', 'shortcode', 'long_url', 'created_at', 'expiry', 'click_count')
    search_fields = ('shortcode', 'long_url')

@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ('id', 'shorturl', 'timestamp', 'referrer', 'location')
    search_fields = ('shorturl__shortcode', 'referrer', 'location')
