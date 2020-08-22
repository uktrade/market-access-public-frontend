from django.urls import path

from .views import FindBarriersSplashView, LocationFiltersView, SectorFiltersView, BarriersListView, BarrierDetailsView

app_name = "barriers"

urlpatterns = [
    path("", FindBarriersSplashView.as_view(), name="find-barriers-splash"),
    path("location/", LocationFiltersView.as_view(), name="choose-location"),
    path("sector/", SectorFiltersView.as_view(), name="choose-sector"),
    path("barriers/", BarriersListView.as_view(), name="list"),
    path("barriers/<int:barrier_id>/", BarrierDetailsView.as_view(), name="details"),
]
