"""OIDC helper"""
import json
from josepy.jws import JWS
from django.utils.encoding import force_bytes
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class IDTokenOIDC(OIDCAuthenticationBackend):
    """Some Providers only include the email in the `id_token`, but not in the userinfo output.
    Hence we merge the id_token data into the userinfo data."""

    def get_userinfo(self, access_token, id_token, payload):
        """Retrive userinfo, parse JWT data, merge the two dictionaries"""
        userdata = super().get_userinfo(access_token, id_token, payload)
        jws = JWS.from_compact(force_bytes(id_token))
        payload = json.loads(jws.payload.decode("utf-8"))
        payload.update(userdata)
        return payload


def generate_username(email):
    """function used to generate OIDC usernames"""
    return email
