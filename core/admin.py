from django.contrib import admin
from core.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'created_at']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'user__username']
    list_filter = ['created_at']
    raw_id_fields = ['user']
