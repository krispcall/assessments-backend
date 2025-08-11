from django.contrib import admin
from accounts.models import User
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