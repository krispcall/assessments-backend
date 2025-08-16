from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone



class CustomAccountManager(BaseUserManager):
    """
    This manager provides methods to create user and superuser accounts.
    Base class:
        - BaseUserManager
    Returns: 
        - create user and superuser instances.
    """
    def create_user(self, email, username, password=None, **other_fields):
        """
        This function will create user
        Args:
            - email (str)
            - username (str)
            - password (optional)
        Kwargs:
            - other_fields
        Returns:
            - user instance
        """
        email = self.normalize_email(email)
        user  = self.model(email=email, username=username, **other_fields)
        if password is None:
            raise ValueError('Password is requried')
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password=None, **other_fields):
        """
        This func will create the super user
        Args:
            - email (str)
            - username (str)
            - password (optional) 
        Kwargs:
            - other_fields 
        Returns:
            - users instance
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is False:
            raise ValueError('Superuser must be assigned is_staff = True')

        if other_fields.get('is_superuser') is False:
            raise ValueError('Superuser must be assigned is_superuser = True')
        if not password:
            raise ValueError('Password is requried')
        user = self.create_user(email=email, username=username, password=password, **other_fields)
        return user
    
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that extends AbstractBaseUser and PermissionsMixin.
    Base classes:
        - AbstractBaseUser
        - PermissionsMixin
    Returns:
        User: A user instance with email as the unique identifier and custom role fields.
    """
    email           = models.EmailField(verbose_name='Email', unique=True)
    username        = models.CharField(verbose_name='Username',max_length=255, unique=True)
    is_active       = models.BooleanField(verbose_name='is active',default=False)
    is_staff        = models.BooleanField(verbose_name='is staff',default=False)
    is_superuser    = models.BooleanField(verbose_name='is superuser',default=False)
    date_joined     = models.DateField(verbose_name='date joined',auto_now_add=True,auto_now=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomAccountManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table='user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    

class Subscription(models.Model):
    """
    Custom User subscription model for package subscription.
    Base classes:
        - Models
    Returns:
        subscription types for the user
    """
    SUBSCRIPTION_TYPE = (
        ("FREE","FREE"),
        ("BASIC","BASIC"),
        ("PRO","PRO"),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='subscription')
    subscription_type = models.CharField(choices=SUBSCRIPTION_TYPE, max_length=55, default="FREE")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscription'
        verbose_name = 'subscription'
        verbose_name_plural = 'subscription'

    def __str__(self):
        return self.subscription_type



class ThrottleLog(models.Model):
    user_id = models.IntegerField(null=True, blank=True)  # store user ID if authenticated
    api_key = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    reason = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.timestamp} | {self.ip_address} | {self.reason}"
    
    class Meta:
        db_table = 'throttlelog'
        verbose_name = 'ThrottleLog'
        verbose_name_plural = 'ThrottleLog'

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255)
    blocked_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.ip_address} - {'Active' if self.is_active else 'Inactive'}"
    
    class Meta:
        db_table = "blockip"
        verbose_name =  "BlockedIP"
        verbose_name_plural =  "BlockedIP"

    @property
    def is_temporary(self):
        """Check if this block is temporary and still active"""
        if self.expires_at:
            return timezone.now() < self.expires_at
        return False

    @property
    def currently_blocked(self):
        """Check if the IP is currently blocked (temporary or permanent)"""
        if not self.is_active:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True