from django.contrib import admin
from core.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    list_display_links = ['id', 'user']
    search_fields = ['user__username', 'user__email']
    list_filter = ['created_at']
    raw_id_fields = ['user']
