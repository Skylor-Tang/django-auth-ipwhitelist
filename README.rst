=======================
django-auth-ipwhitelist
=======================


.. image:: https://img.shields.io/pypi/v/django-auth-ipwhitelist.svg
        :target: https://pypi.python.org/pypi/django-auth-ipwhitelist


Django Auth IP Whitelist is a module for identity verification in Django applications, allowing login via IP address and offering whitelist functionality.

This module enables users to authenticate themselves automatically using their IP address, eliminating the need for traditional username and password login methods. Additionally, it includes whitelist functionality to prohibit users outside the whitelist, enhancing security and control. By combining IP address login with whitelist capabilities, this module provides a simple, secure, and efficient identity verification mechanism for Django applications.


Installation
------------

Install useing pip:

    .. code-block:: bash

        pip install django-auth-ipwhitelist

Configuration
-------------

Add `django_auth_ipwhitelist` to your `INSTALLED_APPS` setting like this:

    .. code-block:: python

        INSTALLED_APPS = [
             ...
             'django_auth_ipwhitelist',
        ]

Add `django_auth_ipwhitelist.middleware.AuthIPWhitelistMiddleware` to your `MIDDLEWARE` setting like this:

    .. code-block:: python

        MIDDLEWARE = [
            ...
            'django_auth_ipwhitelist.middleware.IPWhitelistMiddleware',
        ]

Add `django_auth_ipwhitelist` to your `AUTHENTICATION_BACKENDS` setting like this:

    .. code-block:: python

        AUTHENTICATION_BACKENDS = [
            ...
            'django_auth_ipwhitelist.backends.IPAuthenticationBackend',
        ]

Create `authipwhitelist` database tables by running the following command:

    .. code-block:: bash

        python manage.py migrate django_auth_ipwhitelist

If you need to add default IP addresses to the whitelist, for example, for logging into the Django admin using the default address, you can achieve this by the following settings in settings.py. By default, `127.0.0.1` is already set as default whitelist addresses.

    .. code-block:: python

        AUTH_IP_WHITELIST = {
            'ALLOWED_WHITELISTED_HOSTS': [
                '127.0.0.1',
            ],
        }

Usage
-----

To use this module, simply add the IP address to the whitelist via the Django admin interface. Once the IP address is added to the whitelist, during authentication, the user instance will be retrieved based on the user information associated with the IP. If the user instance does not exist in the system, it will be created using the associated username. If a user attempts to access the application from an IP address not listed in the whitelist, they will be prompted that the IP is unauthorized.


Integration with djangorestframework-simplejwt
----------------------------------------------

This module allows seamless integration of django-auth-ipwhitelist with drf-simplejwt, enabling authentication based on IP whitelist directly through the JWT token, in addition to the traditional username/password mode. Here's how to set it up:

    .. code-block:: python

        # settings.py
        SIMPLE_JWT = {
            ...
            "TOKEN_OBTAIN_SERIALIZER": "django_auth_ipwhitelist.serializers.IPTokenObtainPairSerializer",
        }

