from django.urls import path

from Housing.views import AddCaretakerToBuildingView, AddTenantToBuildingView, BuildingClassView, BuildingDetailView, BuildingFormView, DeleteBuildingView,UpdateBuildingView, UpdateCaretakerView

urlpatterns = [
    path("", BuildingClassView.as_view(), name="building-view"),
    path("register_building/", BuildingFormView.as_view(), name="building-reg_view"),
    path("building/<int:building_id>/", BuildingDetailView.as_view(), name="building-details"),
    path('building/<int:pk>/update/', UpdateBuildingView.as_view(), name='building-update'),
    path('buildings/<int:pk>/delete/', DeleteBuildingView.as_view(), name='delete-building'),
    path('building/<int:building_id>/tenant/create/', AddTenantToBuildingView.as_view(), name='add-tenant'),
    path('building/<int:building_id>/caretaker/create/', AddCaretakerToBuildingView.as_view(), name='add-caretaker'),
    path('caretakers/<int:pk>/update/', UpdateCaretakerView.as_view(), name='update-caretaker'),
]