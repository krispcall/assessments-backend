from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import SubscriptionPlan, APIKey, RequestLog, BlockedEntity, Alert
from .serializers import (
    SubscriptionPlanSerializer,
    APIKeySerializer,
    RequestLogSerializer,
    BlockedEntitySerializer,
    AlertSerializer,
)

# --------------------------
# Subscription Plan ViewSet
# --------------------------
class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]

# --------------------------
# API Key ViewSet
# --------------------------
class APIKeyViewSet(viewsets.ModelViewSet):
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer
    permission_classes = [AllowAny]

# --------------------------
# Request Log ViewSet
# --------------------------
class RequestLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RequestLog.objects.all().order_by("-timestamp")
    serializer_class = RequestLogSerializer
    permission_classes = [AllowAny]

# --------------------------
# Blocked Entity ViewSet
# --------------------------
class BlockedEntityViewSet(viewsets.ModelViewSet):
    queryset = BlockedEntity.objects.all().order_by("-created_at")
    serializer_class = BlockedEntitySerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["post"])
    def unblock(self, request, pk=None):
        blocked = self.get_object()
        blocked.blocked_until = None
        blocked.save()
        return Response({"status": "unblocked"})

# --------------------------
# Alert ViewSet (optional)
# --------------------------
class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alert.objects.all().order_by("-created_at")
    serializer_class = AlertSerializer
    permission_classes = [AllowAny]
