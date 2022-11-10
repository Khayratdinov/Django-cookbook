from django.apps import AppConfig


class FakeAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fake_admin'
