from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

__all__ = ["AdminHoneypotConfig"]


class AdminHoneypotFixConfig(AppConfig):
    name = "project.apps.admin_honeypot_fix"
    label = "admin_honeypot_fix"
    verbose_name = _("Admin Honeypot")
    default_auto_field = "django.db.models.AutoField"
