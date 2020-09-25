from django.urls import path

from .views import (
    FindBarriersSplashView,
    FindActiveBarriers,
    FindResolvedBarriers,
    LocationFiltersView,
    SectorFiltersView,
    BarriersListView,
    BarrierDetailsView,
)

app_name = "barriers"

urlpatterns = [
    path("", FindBarriersSplashView.as_view(), name="find-barriers-splash"),
    path("active/", FindActiveBarriers.as_view(), name="find-active-barriers"),
    path("resolved/", FindResolvedBarriers.as_view(), name="find-resolved-barriers"),
    path("location/", LocationFiltersView.as_view(), name="choose-location"),
    path("sector/", SectorFiltersView.as_view(), name="choose-sector"),
    path("barriers/", BarriersListView.as_view(), name="list"),
    path("barriers/<int:barrier_id>/", BarrierDetailsView.as_view(), name="details"),
]
