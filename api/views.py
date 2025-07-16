from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from .models import ShortURL, Click
from .serializers import ShortURLSerializer
from .logging_middleware import log_event
import string
import random
from datetime import timedelta

def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class ShortURLCreate(APIView):
    def post(self, request):
        long_url = request.data.get("url")
        validity = int(request.data.get("validity", 30))
        shortcode = request.data.get("shortcode") or generate_shortcode()
        if not long_url:
            log_event("backend", "error", "shorturl", "Missing long URL in request")
            return Response({"error": "Missing 'url' field"}, status=400)
        if ShortURL.objects.filter(shortcode=shortcode).exists():
            log_event("backend", "error", "shorturl", f"Shortcode collision: {shortcode}")
            return Response({"error": "Shortcode already exists"}, status=400)

        expiry = timezone.now() + timedelta(minutes=validity)
        obj = ShortURL.objects.create(long_url=long_url, shortcode=shortcode, expiry=expiry)
        log_event("backend", "info", "shorturl", f"ShortURL created: {shortcode}")
        return Response(
            {"shortLink": f"http://localhost:8000/{shortcode}", "expiry": expiry.isoformat()},
            status=201
        )


def redirect_short_url(request, shortcode):
    try:
        url_obj = ShortURL.objects.get(shortcode=shortcode)
        if url_obj.expiry < timezone.now():
            log_event("backend", "error", "redirect", f"Expired link: {shortcode}")
            return JsonResponse({"error": "Link expired"}, status=410)
        url_obj.click_count += 1
        url_obj.save()
        Click.objects.create(
            shorturl=url_obj,
            referrer=request.META.get('HTTP_REFERER', ''),
            location=request.META.get('REMOTE_ADDR', '')  
        )
        log_event("backend", "info", "redirect", f"Redirected: {shortcode}")
        return HttpResponseRedirect(url_obj.long_url)
    except ShortURL.DoesNotExist:
        log_event("backend", "error", "redirect", f"Shortcode not found: {shortcode}")
        return JsonResponse({"error": "Not found"}, status=404)


class ShortURLStats(APIView):
    def get(self, request, shortcode):
        try:
            url_obj = ShortURL.objects.get(shortcode=shortcode)
            clicks = url_obj.clicks.all().values("timestamp", "referrer", "location")
            stats = {
                "click_count": url_obj.click_count,
                "original_url": url_obj.long_url,
                "created_at": url_obj.created_at,
                "expiry": url_obj.expiry,
                "clicks": list(clicks),
            }
            log_event("backend", "info", "stats", f"Stats retrieved: {shortcode}")
            return Response(stats)
        except ShortURL.DoesNotExist:
            log_event("backend", "error", "stats", f"Stats not found: {shortcode}")
            return Response({"error": "Not found"}, status=404)
