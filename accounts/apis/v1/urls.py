from django.urls import path
from accounts.apis.v1 import views as account_apis_v1_views

urlpatterns = [
    path('api/v1/token/', account_apis_v1_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', account_apis_v1_views.CustomTokenRefreshView.as_view(), name='token_refresh'),
]