from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer representing a subscription model with validation.
    Base classes:
        - serializers.ModelSerializer
    Returns:
        - SubscriptionSerializer: A serializer instance for Subscription model.
    """
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'subscription_type']
        read_only_fields = ['created_date', 'updated_date']

    def validate_subscription_type(self, value):
        if not value:
            raise serializers.ValidationError("Subscription type cannot be blank.")
        return value