from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MagazineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project.apps.magazine'
    verbose_name = _("Magazine")

    def ready(self):
        from . import signals
