from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from project.apps.core import views as core_views

urlpatterns = i18n_patterns(
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("management/", admin.site.urls),
    path("js-settings/", core_views.js_settings, name="js_settings"),
    # path("search/", include("haystack.urls")),
)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
