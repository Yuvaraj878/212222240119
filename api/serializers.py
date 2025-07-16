from rest_framework import serializers
from .models import ShortURL

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ('id', 'long_url', 'shortcode', 'created_at', 'expiry', 'click_count')
