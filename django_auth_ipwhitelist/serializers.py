from typing import Any, Dict

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer


User = get_user_model()


class IPTokenObtainSerializer(TokenObtainSerializer):
    """
    Serializer for obtaining IP-based authentication tokens.

    This serializer is used to obtain authentication tokens based on IP address.
    It attempts to authenticate users first using username/password, and if that fails,
    it tries to authenticate based on IP address.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialization method.

        Sets the 'required' attribute of fields to False.

        Parameters:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        super().__init__(*args, **kwargs)

        # Set the 'required' attribute of fields to False
        self.fields[self.username_field].required = False
        self.fields["password"].required = False

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        """
        Validation method.

        Attempts authentication first using username/password,
        if unsuccessful, attempts authentication based on IP address.
        """
        try:
            super().validate(attrs)

        except exceptions.AuthenticationFailed:
            request = self.context["request"]
            authenticate_kwargs = {"ip_address": getattr(request, "ip_address", None)}

            try:
                authenticate_kwargs["request"] = request
            except KeyError:
                pass

            self.user = authenticate(**authenticate_kwargs)

            if not api_settings.USER_AUTHENTICATION_RULE(self.user):
                raise exceptions.AuthenticationFailed(
                    self.error_messages["no_active_account"],
                    "no_active_account",
                )

        return {}


class IPTokenObtainPairSerializer(IPTokenObtainSerializer):
    """
    Serializer for obtaining IP-based authentication token pairs.

    This serializer extends IPTokenObtainSerializer to generate token pairs.
    """

    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the serializer fields and generate the token pair.
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
