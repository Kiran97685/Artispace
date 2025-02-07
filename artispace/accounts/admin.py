from django.contrib import admin
from .models import Artist, CustomUser
from django.contrib.auth.admin import UserAdmin

# Define CustomUserAdmin before registering
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

# Register the CustomUser model after defining the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

# Register Artist model
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bio', 'website_url']
    list_filter = ['user']
    search_fields = ('user__username', 'user__email', 'name')
    ordering = ('user__username',)

    def user_username(self, obj):
        return obj.user.username if obj.user else "N/A"

    def user_email(self, obj):
        return obj.user.email if obj.user else "N/A"

    user_username.short_description = "Username"
    user_email.short_description = "Email"
