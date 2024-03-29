from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AuthenticationConfig(AppConfig):
    name = 'authentication'

    def ready(self):
        import authentication.signals
