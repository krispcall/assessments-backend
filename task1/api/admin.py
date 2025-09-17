from django.contrib import admin
from .models import APIKey, SubscriptionPlan, RequestLog, BlockedEntity, Alert

admin.site.register(SubscriptionPlan)
admin.site.register(APIKey)
admin.site.register(RequestLog)
admin.site.register(BlockedEntity)
admin.site.register(Alert)
