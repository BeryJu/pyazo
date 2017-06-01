import json
from django.contrib.auth import get_user_model
from allaccess.clients import OAuth2Client
from allaccess.views import OAuthCallback

class SupervisrOAuth2Client(OAuth2Client):

    def get_profile_info(self, raw_token):
        "Fetch user profile information."
        try:
            token = json.loads(raw_token)['access_token']
            headers = {
                'Authorization': 'Bearer:%s' % token
            }
            response = self.request('get', self.provider.profile_url, token=raw_token, headers=headers)
            response.raise_for_status()
        except RequestException as e:
            logger.error('Unable to fetch user profile: {0}'.format(e))
            return None
        else:
            return response.json() or response.text

class SupervisrOAuthCallback(OAuthCallback):

    client_class = SupervisrOAuth2Client

    def get_user_id(self, provider, info):
        return info['pk']

    def get_or_create_user(self, provider, access, info):
        User = get_user_model()
        kwargs = {
            User.USERNAME_FIELD: info['email'],
            'email': info['email'],
            'first_name': info['first_name'],
            'password': None
        }
        return User.objects.create_user(**kwargs)
