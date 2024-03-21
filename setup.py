#!/usr/bin/env python

"""The setup script."""

import os
import re
from setuptools import setup, find_packages

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

latest_version = get_version('django_auth_ipwhitelist')

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="tangmeijian",
    author_email='tang1996mei@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Django Auth IP Whitelist is a module for identity verification in Django applications, allowing login via IP address and offering whitelist functionality.",
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['django', 'django_auth_ipwhitelist', 'auth', 'ipwhitelist', 'whitelist', 'ip', 'login'],
    name='django-auth-ipwhitelist',
    packages=find_packages(include=['django_auth_ipwhitelist', 'django_auth_ipwhitelist.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Skylor-Tang/django-auth-ipwhitelist',
    version=latest_version,
    zip_safe=False,
)
