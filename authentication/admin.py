from django.contrib import admin
from .models import (
    User, UserDetail, Role, UserRole, UserMoreInfoKey, UserMoreInfo, 
    UserMoreInfoKeyRole, SecurityEvent, OTP
)
from django.utils.translation import gettext_lazy as _

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
    )

class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'firstname', 'lastname', 'address', 'location')
    search_fields = ('firstname', 'lastname', 'user__username', 'user__email', 'user__phone_number')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
    search_fields = ('user__username', 'role__name')

class UserMoreInfoKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class UserMoreInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'key', 'value', 'role')
    search_fields = ('user__username', 'key__name', 'role__name')

class UserMoreInfoKeyRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'role')
    search_fields = ('key__name', 'role__name')

class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ip', 'login_time', 'logout_time', 'logout_reason', 'agent')
    search_fields = ('user__username', 'ip', 'agent')
    list_filter = ('login_time', 'logout_time')

class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'value', 'created_at', 'is_active')
    search_fields = ('user__username', 'value')
    list_filter = ('is_active', 'created_at')

# Register models in admin site
admin.site.register(User, UserAdmin)
admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(UserMoreInfoKey, UserMoreInfoKeyAdmin)
admin.site.register(UserMoreInfo, UserMoreInfoAdmin)
admin.site.register(UserMoreInfoKeyRole, UserMoreInfoKeyRoleAdmin)
admin.site.register(SecurityEvent, SecurityEventAdmin)
admin.site.register(OTP, OTPAdmin)
