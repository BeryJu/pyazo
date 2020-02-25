"""pyazo auth views"""
from django.contrib.auth.views import LoginView

from pyazo.utils.config import CONFIG


class CustomLoginView(LoginView):
    """Custom LoginView that adds `is_oidc` to template, to check if OIDC is enabled."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # SHow OIDC login button
        if CONFIG.y("oidc.client_id", None):
            context["is_oidc"] = True

        return context
