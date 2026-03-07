from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    # clinic_pk is captured by the parent: clinics/<int:clinic_pk>/inventory/
    # and passed through to inventory_add_view(request, clinic_pk)
    path(
        "add/",
        views.inventory_add_view,
        name="add_inventory_item",
    ),

    # item_pk captured here, clinic_pk still comes from the parent
    path(
        "<int:item_pk>/edit/",
        views.inventory_edit_view,
        name="update_inventory_item",
    ),
]