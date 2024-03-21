from django.contrib import admin

from django_auth_ipwhitelist.models import AuthIPWhitelist


@admin.register(AuthIPWhitelist)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "username", "is_active")
