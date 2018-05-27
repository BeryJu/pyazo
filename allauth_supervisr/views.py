"""supervisr adapter"""
import requests
from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2CallbackView,
                                                          OAuth2LoginView)

from allauth_supervisr.provider import SupervisrProvider


class SupervisrOAuth2Adapter(OAuth2Adapter):
    """supervisr OAuth2 Adapter"""
    provider_id = SupervisrProvider.id
    settings = app_settings.PROVIDERS.get(provider_id, {}) # noqa
    provider_base_url = settings.get("SUPERVISR_URL", 'https://my.beryju.org')

    access_token_url = '{0}/app/mod/auth/oauth/provider/token/'.format(provider_base_url)
    authorize_url = '{0}/app/mod/auth/oauth/provider/authorize/'.format(provider_base_url)
    profile_url = '{0}/api/core/v1/accounts/me/?format=openid'.format(
        provider_base_url)


    def complete_login(self, request, app, token, **kwargs):
        headers = {
            'Authorization': 'Bearer {0}'.format(token.token),
            'Content-Type': 'application/json',
        }
        extra_data = requests.get(self.profile_url, headers=headers)

        return self.get_provider().sociallogin_from_response(
            request,
            extra_data.json()
        )


oauth2_login = OAuth2LoginView.adapter_view(SupervisrOAuth2Adapter) # noqa
oauth2_callback = OAuth2CallbackView.adapter_view(SupervisrOAuth2Adapter) # noqa
