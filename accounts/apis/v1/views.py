from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View for obtaining JWT access and refresh tokens.
    Base classes:
        - TokenObtainPairView
    Returns:
        - CustomTokenObtainPairView: Provides JWT tokens (access and refresh) upon valid user authentication.
    """
    @swagger_auto_schema(
        operation_summary="Featch JWT Token Pair with basic Credential",
        tags=['Authentication Endpoints'],
        operation_description="Obtain a new pair of access and refresh tokens by providing valid user credentials.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                },
                description='Tokens successfully obtained',
            ),
            401: 'Unauthorized - Invalid credentials',
        },
        security=[],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomTokenRefreshView(TokenRefreshView):
    """
    View for refreshing the JWT access token using a valid refresh token.
    Base classes:
        - TokenRefreshView
    Returns:
        - CustomTokenRefreshView: Provides a new access token upon receiving a valid refresh token.
    """
    @swagger_auto_schema(
        operation_summary="Obtain access token via refresh token",
        tags=['Authentication Endpoints'],
        operation_description="Refresh the JWT access token by providing a valid refresh token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='New access token'),
                },
                description='Access token refreshed successfully',
            ),
            401: 'Unauthorized - Invalid or expired refresh token',
        },
        security=[],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)