from drf_yasg import openapi
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from accounts.apis.v1.serializers import (
    SubscriptionSerializer,
)
from accounts.models import Subscription
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


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
    


class SubscriptionView(viewsets.ViewSet):
    """
    Handles CRUD operations for subscription model.
    Base classes:
        - viewsets.ViewSet
    Returns:
        -  return information about the package subscription.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="subscribe the package",
        operation_description="here subscription is created",
        request_body=SubscriptionSerializer,
        tags=["Subscription Endpoints"],
        security=[{'Bearer': []}]
    )
    def create(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            response = {
                'success': True,
                'data': serializer.data,
                'message':'successfully subscribed package'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'sucess': False,
            'data' : serializer.errors,
            'message':"Unable to subscribe the package"           
            }
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="unsubscribe the package",
        operation_description="here subscription is deleted",
        request_body=None,
        tags=["Subscription Endpoints"],
        security=[{'Bearer': []}]
    )
    def destroy(self, request, pk=None):
        try:
            subscription = Subscription.objects.get(pk=pk)
            subscription.delete()
            response = {
                'success': True,
                'message': 'Successfully unsubscribed the package'
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        except Subscription.DoesNotExist:
            response = {
                'success': False,
                'message': 'Subscription not found'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            response = {
                'success': False,
                'data': e,
                'message': f'Unable to unsubscribe the package'
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)