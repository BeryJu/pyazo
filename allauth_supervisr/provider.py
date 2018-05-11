"""supervisr provider"""
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class SupervisrAccount(ProviderAccount):
    """supervisr account"""

    def to_str(self):
        dflt = super(SupervisrAccount, self).to_str()
        return self.account.extra_data.get('username', dflt)


class SupervisrProvider(OAuth2Provider):
    """supervisr provider"""

    id = 'supervisr'
    name = 'Supervisr'
    account_class = SupervisrAccount

    def extract_uid(self, data):
        return str(data['sub'])

    def extract_common_fields(self, data):
        return dict(
            email=data.get('email'),
            username=data.get('preferred_username'),
            name=data.get('name'),
        )

    def get_default_scope(self):
        return ['read']


provider_classes = [SupervisrProvider] # noqa
