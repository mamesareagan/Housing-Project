from django.urls import path

from Housing.views import AddTenantToBuildingView, BuildingClassView, BuildingDetailView, BuildingFormView,UpdateBuildingView

urlpatterns = [
    path("", BuildingClassView.as_view(), name="building-view"),
    path("register_building/", BuildingFormView.as_view(), name="building-reg_view"),
    path("building/<int:building_id>/", BuildingDetailView.as_view(), name="building-details"),
    path('building/<int:pk>/update/', UpdateBuildingView.as_view(), name='building-update'),
    path('building/<int:building_id>/tenant/create/', AddTenantToBuildingView.as_view(), name='add-tenant'),
]