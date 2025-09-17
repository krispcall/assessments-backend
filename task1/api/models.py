from django.db import models
from django.contrib.auth.models import User

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
    ("free", "Free"),
    ("basic", "Basic"),
    ("pro", "Pro"),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    daily_limit = models.IntegerField(null=True, blank=True, help_text="Null = Unlimited")

    def __str__(self):
        return f"{self.get_name_display()} ({'Unlimited' if not self.daily_limit else self.daily_limit})"


class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, unique=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.key[:8]}..."


class RequestLog(models.Model):
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.api_key} @ {self.ip_address} - {self.timestamp}"


class BlockedEntity(models.Model):
    ENTITY_TYPE_CHOICES = [
    ("user", "User"),
    ("ip", "IP"),
    ]
    entity_type = models.CharField(max_length=10, choices=ENTITY_TYPE_CHOICES)
    value = models.CharField(max_length=255) # user_id or IP address
    reason = models.TextField(blank=True, null=True)
    blocked_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("entity_type", "value")

    def __str__(self):
        return f"{self.entity_type}: {self.value} (until {self.blocked_until})"


class Alert(models.Model):
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=[("webhook", "Webhook"), ("email", "Email")])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.api_key} - {self.alert_type}"