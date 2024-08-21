from django.urls import path, include
from .views import add_material, all_materials, details, edit_material, index, base, material_usage
from rest_framework.routers import DefaultRouter
from .views import  MaterialDetailview, MaterialAllView

router = DefaultRouter()

app_name = "Tuzimbe"

urlpatterns = [
    path("", index, name="index"),
    path("base", base, name="base"),
    path("addmaterials/", add_material, name="addmaterials"),
    path("materials/", all_materials, name="materials"),
    path('material/<int:id>/details/', details, name="details"),
    path('material/<int:id>/edit/', edit_material, name="edit"),
    path('material/usage/', material_usage, name="material_usage"),


    path('api/', include(router.urls)),
    path('api/materials/', MaterialAllView.as_view(), name='material_create'),
    path('api/materials/detail/<int:id>/', MaterialDetailview.as_view(), name='material_detail'),
]