import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from .models import APIKey
from .utils import RateLimiter


class RateLimitMiddleware(MiddlewareMixin):
    """
    Middleware to handle API key authentication and rate limiting.
    """

    def process_request(self, request):
        """
        Processes each incoming request to check for API key validity and rate limits.
        """
        # Extract API key from request headers
        api_key_value = request.headers.get("X-API-Key")
        
        try:
            api_key = APIKey.objects.get(key=api_key_value, is_active=True)
        except APIKey.DoesNotExist:
            return JsonResponse({"detail": "Invalid or inactive API Key."}, status=403)

        # Extract client IP
        ip_address = self.get_client_ip(request)

        # Run rate limiter
        limiter = RateLimiter(api_key, ip_address)
        allowed, message = limiter.allow_request()

        if not allowed:
            return JsonResponse({"detail": message}, status=429)  # 429 = Too Many Requests

        # Attach api_key to request for later use in views
        request.api_key = api_key

    def get_client_ip(self, request):
        """Extract client IP from request headers."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # The first IP in the list is the real client IP
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")