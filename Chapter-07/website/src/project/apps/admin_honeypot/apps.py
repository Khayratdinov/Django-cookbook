from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# __all__ = ["AdminHoneypotConfig"]


class AdminHoneypotConfig(AppConfig):
    name = "project.apps.admin_honeypot"
    verbose_name = _("Admin Honeypot")
