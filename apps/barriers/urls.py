from django.urls import path

from .views import FindBarriersSplashView, LocationFiltersView, SectorFiltersView

app_name = "barriers"

urlpatterns = [
    path("", FindBarriersSplashView.as_view(), name="find-barriers-splash"),
    path("location/", LocationFiltersView.as_view(), name="choose-location"),
    path("sector/", SectorFiltersView.as_view(), name="choose-sector"),
]
