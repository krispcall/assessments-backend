from rest_framework.throttling import BaseThrottle
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.core.cache import cache

PLAN_LIMITS = {
    "FREE": 100,
    "BASIC": 1000,
    "PRO": None,
}

BURST_LIMIT = 15  
BURST_WINDOW_SEC = 60  


class CustomRateThrottle(BaseThrottle):
    """
    Custom throttle based on subscription type.
    Tracks requests per user per day.
    Also temporary blocks if too many requests in short time.
    """
    def allow_request(self, request, view):
        user = request.user
        if not user.is_authenticated:
            raise ValidationError("Authentication required.")
        if not hasattr(user, "subscription"):
            raise ValidationError("please subscribe !!!")
        subscription_type = user.subscription.subscription_type
        limit = PLAN_LIMITS.get(subscription_type)
        burst_key = f"burst_{user.id}"
        burst_count = cache.get(burst_key, 0)
        if burst_count >= BURST_LIMIT:
            raise ValidationError(
                "Too many requests in a short time. Try again later."
            )
        cache.set(burst_key, burst_count + 1, timeout=BURST_WINDOW_SEC)
        if limit is None:
            return True
        today_key = f"throttle_{user.id}_{timezone.now().date()}"
        request_count = cache.get(today_key, 0)
        if request_count >= limit:
            raise ValidationError(
                f"Daily limit reached for {subscription_type} plan. Limit: {limit}"
            )
        cache.set(today_key, request_count + 1, timeout=86400)
        return True
