from django.db import models


class AuthIPWhitelist(models.Model):
    """
    Model to store allowed IP addresses and their associated users.
    This model is used by django-auth-ipwhitelist.

    Attributes:
        ip_address (str): The IP address to whitelist.
        is_active (bool): Flag indicating whether the IP address is active or not.
        username (str, optional): The associated username if available.
    """

    ip_address = models.GenericIPAddressField(unique=True)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.ip_address}: {'available' if self.is_active else 'not available'}"
