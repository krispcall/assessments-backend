from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.apis.v1 import views as account_apis_v1_views
from accounts.apis.v1.views import SubscriptionView

app_name = 'accounts_apis_v1'

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionView, basename='subscription')

urlpatterns = [
    path('api/v1/token/', account_apis_v1_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', account_apis_v1_views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include(router.urls)),
]
