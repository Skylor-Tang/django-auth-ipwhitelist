from django.http import JsonResponse

from django_auth_ipwhitelist.models import AuthIPWhitelist
from django_auth_ipwhitelist.settings import auth_ip_whitelist_settings


class AuthIPWhitelistMiddleware:
    """
    Middleware to whitelist IP addresses for authentication in Django.

    This middleware checks if the client's IP address is whitelisted before allowing access to the application.
    If the IP address is not whitelisted, a 403 Forbidden response is returned.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def get_client_ip(self, request):
        """
        Retrieves the client's IP address from the request.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]

        else:
            ip = request.META.get("REMOTE_ADDR")

        return ip

    def __call__(self, request):
        """
        The middleware's main logic that checks if the IP address is whitelisted.
        """
        client_ip = self.get_client_ip(request)

        # Get the list of whitelisted IP addresses, including the ones from the database(AuthIPWhitelist) and the settings
        allowed_whitelist_host = getattr(auth_ip_whitelist_settings, "ALLOWED_WHITELISTED_HOSTS", [])
        ip_whitelist = set([entry.ip_address for entry in AuthIPWhitelist.objects.filter(is_active=True)] + allowed_whitelist_host)

        if client_ip not in ip_whitelist:
            return JsonResponse({"detail": "Access Forbidden: Your IP is not whitelisted."}, status=403)

        # Set the login IP address to match the detected IP address
        request.ip_address = client_ip

        response = self.get_response(request)
        return response
