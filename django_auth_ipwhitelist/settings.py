from django.conf import settings
from django.test.signals import setting_changed


DEFAULTS = {
    'ALLOWED_WHITELISTED_HOSTS': [
        '127.0.0.1',
    ],
}


class AuthIPWhitelistSettings:
    """
    The implementation is derived from the django-rest-framework framework.

    A settings object that allows Auth IPWhitelist settings to be accessed as
    properties. For example:

        from django_auth_ipwhitelist.settings import auth_ip_whitelist_settings
        print(auth_ip_whitelist_settings.ALLOWED_WHITELISTED_HOSTS)

    """
    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'AUTH_IP_WHITELIST', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid auth ip whitelist setting: '%s'" % attr)

        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]

        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()

        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


auth_ip_whitelist_settings = AuthIPWhitelistSettings(None, DEFAULTS)


def reload_auth_ip_whitelist_settings(*args, **kwargs):
    """
    Reloads the Auth IP Whitelist settings.

    This function is called when the 'AUTH_IP_WHITELIST' setting is changed.
    It triggers the reload of the settings.
    """
    setting = kwargs['setting']
    if setting == 'AUTH_IP_WHITELIST':
        auth_ip_whitelist_settings.reload()


setting_changed.connect(reload_auth_ip_whitelist_settings)
