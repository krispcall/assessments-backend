from django.contrib import admin
from accounts.models import User, Subscription, BlockedIP, ThrottleLog
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserADmin(UserAdmin):
    """
    This class show the usermodel data into the admin panel

    Args:
        - BaseClass: UserAdmin
    Returns:
        - None
    """
    list_display=['id','email','username','is_staff','is_active','date_joined']
    list_display_links=['id','email',]
    list_filter = ['is_active','is_staff','is_superuser','date_joined']
    readonly_fields = ('date_joined','last_login')
    search_fields = ['email','username']
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ( 'email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff','is_superuser','groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2'),
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    This class show the subscription data into the admin panel
    Args:
        - BaseClass: ModelAdmin
    Returns:
        - None
    """
    list_display=['user','subscription_type','created_date','updated_date']
    list_display_links=['user','subscription_type','created_date','updated_date']
    list_filter = ['subscription_type',]
    search_fields = ['subscription_type',]
    readonly_fields = ('created_date', 'updated_date')

    fieldsets = (
        (_('User Details'), {'fields': ( 'user',)}),
        (_('Subscription Package'), {'fields': ( 'subscription_type',)}),
        (_('Important dates'), {'fields': ('created_date', 'updated_date')}),
    )
    
    # we can enable or disbale this as per our need
    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_add_permission(self, request):
        return 
    
    def has_change_permission(self, request, obj=None):
        return True
    

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "reason", "blocked_at", "expires_at", "is_active")
    list_filter = ("is_active", "blocked_at")
    search_fields = ("ip_address",)
    actions = ["unblock_ips"]

    def unblock_ips(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected IPs have been unblocked.")
    unblock_ips.short_description = "Unblock selected IPs"


@admin.register(ThrottleLog)
class ThrottleLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user_id", "api_key", "ip_address", "reason")
    list_filter = ("timestamp", "ip_address")
    search_fields = ("user_id", "api_key", "ip_address", "reason")