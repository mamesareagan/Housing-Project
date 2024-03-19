from django.urls import path

from Housing.views import BuildingClassView, BuildingFormView

urlpatterns = [
    path("", BuildingClassView.as_view(), name="building-view"),
    path("register_building/", BuildingFormView.as_view(), name="building-reg_view"),
]