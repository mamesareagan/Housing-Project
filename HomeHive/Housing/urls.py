from django.urls import path

from Housing.views import BuildingClassView

urlpatterns = [
    path("", BuildingClassView.as_view(), name="building-view"),
]