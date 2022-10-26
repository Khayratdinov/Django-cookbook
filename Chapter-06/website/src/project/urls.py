from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from project.apps.core import views as core_views

urlpatterns = i18n_patterns(
    path("", lambda request: redirect("locations:location_list")),
    # path("", lambda request: redirect("ideas:idea_list")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ideas/", include(("project.apps.ideas.urls", "ideas"), namespace="ideas")),
    path("js-settings/", core_views.js_settings, name="js_settings"),
    path(
        "locations/",
        include(("project.apps.locations.urls", "locations"), namespace="locations"),
    ),
    path("likes/", include(("project.apps.likes.urls", "likes"), namespace="likes")),
    # path("search/", include("haystack.urls")),
)


urlpatterns += [
    path(
        "upload-file/",
        core_views.upload_file,
        name="upload_file",
    ),
    path(
        "delete-file/",
        core_views.delete_file,
        name="delete_file",
    ),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)
