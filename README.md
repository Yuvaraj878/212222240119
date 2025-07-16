<H3> Name : Yuvaraj S </H3>
<H3> Register No : 212222240119 </H3>
<H3> Project : URL Shortener Microservice </H3>

<h1 align="center">Implementation of a URL Shortener Microservice with Analytics and Custom Logging</h1>

---

## Aim:

To design and implement a scalable URL Shortener backend microservice using Django, with analytics tracking and custom logging middleware.

---

## Algorithm / Implementation Steps:

### Step 1:
Set up a Django project and create the necessary app structure for the URL shortener service.

### Step 2:
Define Django models for storing shortened URLs and click analytics, including fields for expiry and click tracking.

### Step 3:
Build REST API endpoints to:
- Create a short URL (`/shorturls`, POST)
- Redirect to the original URL (`/<shortcode>`, GET)
- Fetch analytics (`/shorturls/<shortcode>`, GET)

### Step 4:
Implement custom logging middleware to send all logs to the specified logging API, instead of using Django's default logging.

### Step 5:
Add proper error handling for cases like expired URLs, duplicate shortcodes, and invalid requests.

### Step 6:
Integrate analytics collection on each redirect (count, referrer, timestamp, IP).

### Step 7:
Test all endpoints with multiple input scenarios and verify results via API responses and Django admin.

---

## Program:

<details>
<summary><b>Click to view key code snippets</b></summary>

```python
# models.py

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
# Example view for creating a short URL (views.py)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import ShortURL
import string, random
from datetime import timedelta
from .logging_middleware import log_event

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
```
</details>

