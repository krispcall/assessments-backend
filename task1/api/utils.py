import datetime
from django.utils import timezone
from django.db.models import Count
from api.models import APIKey, RequestLog, BlockedEntity, SubscriptionPlan  # adjust import path

class RateLimiter:
    def __init__(self, api_key: APIKey, ip_address: str):
        self.api_key = api_key
        self.ip_address = ip_address

    def log_request(self):
        """Log every request for tracking and analytics"""
        RequestLog.objects.create(api_key=self.api_key, ip_address=self.ip_address)

    def is_blocked(self):
        """Check if user or IP is currently blocked"""
        now = timezone.now()
        blocked_user = BlockedEntity.objects.filter(
        entity_type="user", value=str(self.api_key.user.id), blocked_until__gt=now
        ).exists()
        blocked_ip = BlockedEntity.objects.filter(
        entity_type="ip", value=self.ip_address, blocked_until__gt=now
        ).exists()
        return blocked_user or blocked_ip

    def check_daily_limit(self):
        """Check subscription plan daily limits"""
        plan = self.api_key.plan
        if plan.daily_limit is None:  # Unlimited
            return True

        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        request_count = RequestLog.objects.filter(
            api_key=self.api_key, timestamp__gte=today_start
        ).count()

        return request_count < plan.daily_limit

    def detect_abuse(self):
        """Detect suspicious activity like spam requests or API key switching"""
        now = timezone.now()
        one_minute_ago = now - datetime.timedelta(minutes=1)

        # Too many requests in short time
        recent_requests = RequestLog.objects.filter(
            ip_address=self.ip_address, timestamp__gte=one_minute_ago
        ).count()
        if recent_requests > 50:  # threshold, can be tuned
            self.block_entity("ip", self.ip_address, reason="Too many requests per minute")
            return False

        # API key switching from same IP
        unique_keys = (
            RequestLog.objects.filter(ip_address=self.ip_address, timestamp__gte=one_minute_ago)
            .values("api_key")
            .distinct()
            .count()
        )
        if unique_keys > 5:  # suspicious API key switching
            self.block_entity("ip", self.ip_address, reason="Suspicious API key switching")
            return False

        return True

    def block_entity(self, entity_type: str, value: str, reason: str, duration_minutes: int = 60):
        """Temporarily block a user or IP"""
        BlockedEntity.objects.update_or_create(
            entity_type=entity_type,
            value=value,
            defaults={
                "reason": reason,
                "blocked_until": timezone.now() + datetime.timedelta(minutes=duration_minutes),
            },
        )

    def allow_request(self):
        """Main entrypoint: check all conditions before allowing"""
        if self.is_blocked():
            return False, "Blocked due to suspicious activity"

        if not self.check_daily_limit():
            self.block_entity("user", str(self.api_key.user.id), "Exceeded daily limit", duration_minutes=1440)
            return False, "Daily request limit exceeded"

        if not self.detect_abuse():
            return False, "Abuse detected"

        # Passed all checks → log request
        self.log_request()
        return True, "Request allowed"
