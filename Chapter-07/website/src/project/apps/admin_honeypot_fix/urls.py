from . import views
from django.urls import path, re_path

app_name = "admin_honeypot_fix"

urlpatterns = [
    path("login/", views.AdminHoneypot.as_view(), name="login"),
    re_path(r"^.*$", views.AdminHoneypot.as_view(), name="index"),
]
