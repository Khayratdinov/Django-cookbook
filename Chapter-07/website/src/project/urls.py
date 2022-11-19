from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from project.apps.external_auth import views

urlpatterns = i18n_patterns(
    # path("", lambda request: redirect("ideas:idea_list")),
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout, name="auth0_logout"),
    path("", include("social_django.urls")), 
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "admin/",
        include("project.apps.admin_honeypot.urls", namespace="admin_honeypot_fix"),
    ),
    path("secret/", admin.site.urls),
    path("ideas/", include(("project.apps.ideas.urls", "ideas"), namespace="ideas")),
    # path("search/", include("haystack.urls")),
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
