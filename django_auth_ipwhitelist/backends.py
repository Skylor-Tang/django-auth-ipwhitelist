from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from django_auth_ipwhitelist.models import AuthIPWhitelist


UserModel = get_user_model()


class IPAuthenticationBackend(ModelBackend):
    create_unknown_user = True

    def authenticate(self, request, ip_address):
        """
        Authenticates a user based on the provided IP address.

        Args:
            request (HttpRequest): The current request object.
            ip_address (str): The IP address to authenticate.

        Returns:
            User: The authenticated user object if found, None otherwise.
        """
        if not ip_address:
            return

        created = False
        user = None

        if username := self.get_username_from_AuthIPWhitelist(ip_address):
            # Note that this could be accomplished in one try-except clause, but
            # instead we use get_or_create when creating unknown users since it has
            # built-in safeguards for multiple threads.
            if self.create_unknown_user:
                user, created = UserModel._default_manager.get_or_create(**{UserModel.USERNAME_FIELD: username})
            else:
                try:
                    user = UserModel._default_manager.get_by_natural_key(username)
                except UserModel.DoesNotExist:
                    pass

            user = self.configure_user(request, user, created=created)

            return user if self.user_can_authenticate(user) else None

        return None

    def configure_user(self, request, user, created=True):
        """
        Configures a user and returns the updated user.

        By default, returns the user unmodified.

        Args:
            request (HttpRequest): The current request object.
            user (User): The user object to configure.
            created (bool, optional): Indicates if the user was just created. Defaults to True.

        Returns:
            User: The updated user object.
        """
        return user

    def get_username_from_AuthIPWhitelist(self, ip_address):
        """
        Retrieves the username associated with the provided IP address from the AuthIPWhitelist model.

        Args:
            ip_address (str): The IP address to retrieve the username for.

        Returns:
            str: The username associated with the IP address if found, None otherwise.
        """
        try:
            obj = AuthIPWhitelist.objects.get(Q(is_active=True) & Q(ip_address=ip_address))
            return obj.username

        except AuthIPWhitelist.DoesNotExist:
            return
