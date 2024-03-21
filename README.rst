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
            'django_auth_ipwhitelist.middleware.AuthIPWhitelistMiddleware',
        ]