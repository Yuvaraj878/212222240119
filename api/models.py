from django.db import models

class ShortURL(models.Model):
    long_url = models.URLField()
    shortcode = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    click_count = models.IntegerField(default=0)

class Click(models.Model):
    shorturl = models.ForeignKey(ShortURL, related_name='clicks', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=100, blank=True)
