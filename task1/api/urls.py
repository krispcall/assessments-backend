from django.urls import path
from .views import (
    SubscriptionPlanViewSet,
    APIKeyViewSet,
    RequestLogViewSet,
    BlockedEntityViewSet,
    AlertViewSet,
)

# --------------------------
# Subscription Plans
# --------------------------
subscription_plan_list = SubscriptionPlanViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
subscription_plan_detail = SubscriptionPlanViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# --------------------------
# API Keys
# --------------------------
api_key_list = APIKeyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
api_key_detail = APIKeyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# --------------------------
# Request Logs (read-only)
# --------------------------
request_log_list = RequestLogViewSet.as_view({
    'get': 'list'
})
request_log_detail = RequestLogViewSet.as_view({
    'get': 'retrieve'
})

# --------------------------
# Blocked Entities
# --------------------------
blocked_entity_list = BlockedEntityViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
blocked_entity_detail = BlockedEntityViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
blocked_entity_unblock = BlockedEntityViewSet.as_view({
    'post': 'unblock'
})

# --------------------------
# Alerts (read-only)
# --------------------------
alert_list = AlertViewSet.as_view({
    'get': 'list'
})
alert_detail = AlertViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    # Subscription Plan
    path('subscription-plans/', subscription_plan_list, name='subscriptionplan-list'),
    path('subscription-plans/<int:pk>/', subscription_plan_detail, name='subscriptionplan-detail'),

    # API Key
    path('api-keys/', api_key_list, name='apikey-list'),
    path('api-keys/<int:pk>/', api_key_detail, name='apikey-detail'),

    # Request Logs
    path('request-logs/', request_log_list, name='requestlog-list'),
    path('request-logs/<int:pk>/', request_log_detail, name='requestlog-detail'),

    # Blocked Entities
    path('blocked-entities/', blocked_entity_list, name='blockedentity-list'),
    path('blocked-entities/<int:pk>/', blocked_entity_detail, name='blockedentity-detail'),
    path('blocked-entities/<int:pk>/unblock/', blocked_entity_unblock, name='blockedentity-unblock'),

    # Alerts
    path('alerts/', alert_list, name='alert-list'),
    path('alerts/<int:pk>/', alert_detail, name='alert-detail'),
]
