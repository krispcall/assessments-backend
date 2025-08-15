from rest_framework.throttling import BaseThrottle
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta
from accounts.models import BlockedIP, ThrottleLog

PLAN_LIMITS = {
    "FREE": 100,
    "BASIC": 1000,
    "PRO": None,
}

BURST_LIMIT = 60
BURST_WINDOW_SEC = 60

JWT_SWITCH_LIMIT = 5
JWT_SWITCH_WINDOW = 60

TEMP_BLOCK_TIME = 3600
ALERT_THRESHOLD = 0.8 
class CustomRateThrottle(BaseThrottle):
    def allow_request(self, request, view):
        user = request.user
        ip = self.get_client_ip(request)
        jwt_token = self.get_jwt_from_request(request)
        user_id = user.id if user.is_authenticated else None
        api_key = jwt_token
        blocked = BlockedIP.objects.filter(ip_address=ip, is_active=True).first()
        if blocked and blocked.currently_blocked:
            ThrottleLog.objects.create(
                user_id=user_id,
                api_key=api_key,
                ip_address=ip,
                reason=f"Blocked IP access: {blocked.reason}"
            )
            raise ValidationError(f"This IP is blocked: {blocked.reason}")
        if jwt_token:
            ip_jwt_key = f"ip_jwts_{ip}"
            jwt_set = cache.get(ip_jwt_key, set())
            jwt_set.add(jwt_token)
            cache.set(ip_jwt_key, jwt_set, timeout=JWT_SWITCH_WINDOW)
            if len(jwt_set) > JWT_SWITCH_LIMIT:
                BlockedIP.objects.get_or_create(
                    ip_address=ip,
                    defaults={
                        "reason": "Rapid JWT switching (permanent)",
                        "blocked_at": timezone.now(),
                        "expires_at": None,
                        "is_active": True
                    }
                )
                ThrottleLog.objects.create(
                    user_id=user_id,
                    api_key=api_key,
                    ip_address=ip,
                    reason="Rapid JWT switching - permanently blocked"
                )
                raise ValidationError("This IP has been permanently blocked due to abuse.")
        if user.is_authenticated:
            burst_key = f"burst_{user.id}"
            burst_count = cache.get(burst_key, 0)
            if burst_count >= BURST_LIMIT:
                BlockedIP.objects.create(
                    ip_address=ip,
                    reason="Burst request limit exceeded (temporary)",
                    blocked_at=timezone.now(),
                    expires_at=timezone.now() + timedelta(seconds=TEMP_BLOCK_TIME)
                )
                ThrottleLog.objects.create(
                    user_id=user_id,
                    api_key=api_key,
                    ip_address=ip,
                    reason="Burst limit exceeded - temporarily blocked"
                )
                raise ValidationError("Too many requests in a short time. IP temporarily blocked.")
            cache.set(burst_key, burst_count + 1, timeout=BURST_WINDOW_SEC)
        if user.is_authenticated and PLAN_LIMITS.get(user.subscription.subscription_type) is not None:
            limit = PLAN_LIMITS[user.subscription.subscription_type]
            today_key = f"throttle_{user.id}_{timezone.now().date()}"
            request_count = cache.get(today_key, 0)
            request_count += 1
            cache.set(today_key, request_count, timeout=86400)
            alert_threshold = int(limit * ALERT_THRESHOLD)
            if request_count == alert_threshold:
                ThrottleLog.objects.create(
                    user_id=user_id,
                    api_key=api_key,
                    ip_address=ip,
                    reason=f"Approaching daily limit ({request_count}/{limit})"
                )
                print(f"Alert: User {user_id} reached {alert_threshold}/{limit} requests")  # optional
            if request_count > limit:
                BlockedIP.objects.create(
                    ip_address=ip,
                    reason=f"Daily limit exceeded ({limit} requests)",
                    blocked_at=timezone.now(),
                    expires_at=timezone.now() + timedelta(seconds=TEMP_BLOCK_TIME)
                )
                ThrottleLog.objects.create(
                    user_id=user_id,
                    api_key=api_key,
                    ip_address=ip,
                    reason=f"Daily limit exceeded ({limit} requests)"
                )
                raise ValidationError(f"Daily limit reached for {user.subscription.subscription_type} plan. Limit: {limit}")
        return True

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_jwt_from_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None
