from django.urls import path
from .views import LocationList, LocationDetail


urlpatterns = [
    path("", LocationList.as_view(), name="location_list"),
    # path("add/", add_or_change_location, name="add_location"),
    path("<uuid:pk>/", LocationDetail.as_view(), name="location_detail"),
    path(
        "<uuid:pk>/modal/",
        LocationDetail.as_view(
            template_name="locations/location_detail_modal.html"),
        name="location_detail_modal",
    ),
]
