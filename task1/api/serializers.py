from rest_framework import serializers
from .models import SubscriptionPlan, APIKey, RequestLog, BlockedEntity, Alert

# --------------------------
# Subscription Plan Serializer
# --------------------------
class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ["id", "name", "daily_limit", "created_at"]
        read_only_fields = ["id", "created_at"]

# --------------------------
# API Key Serializer
# --------------------------
class APIKeySerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = APIKey
        fields = ["id", "user", "key", "plan", "is_active", "created_at"]
        read_only_fields = ["id", "created_at", "key"]

# --------------------------
# Request Log Serializer
# --------------------------
class RequestLogSerializer(serializers.ModelSerializer):
    api_key = APIKeySerializer(read_only=True)

    class Meta:
        model = RequestLog
        fields = ["id", "api_key", "ip_address", "timestamp"]
        read_only_fields = ["id", "api_key", "timestamp"]

# --------------------------
# Blocked Entity Serializer
# --------------------------
class BlockedEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedEntity
        fields = ["id", "entity_type", "value", "reason", "blocked_until", "created_at"]
        read_only_fields = ["id", "created_at"]

# --------------------------
# Alert Serializer (optional)
# --------------------------
class AlertSerializer(serializers.ModelSerializer):
    api_key = APIKeySerializer(read_only=True)

    class Meta:
        model = Alert
        fields = ["id", "api_key", "alert_type", "message", "created_at"]
        read_only_fields = ["id", "created_at"]
