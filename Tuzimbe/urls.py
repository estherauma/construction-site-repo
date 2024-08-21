from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import index, base, add_workers,all_workers,update_workers,worker_details,delete_workers,worker_attendance,attendance_list,update_attendance, add_material, all_materials, details, edit_material, material_usage
from .views import WorkerListAPIView, WorkerDetailAPIView, WorkerUpdateAPIView, WorkerCreateAPIView, RegisterWorkerAPIView, MaterialAllView, MaterialDetailview
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
    path("add-workers/", add_workers, name="add-workers"),
    path("all-workers/", all_workers, name="all-workers"),
    path("update-workers/<int:pk>/", update_workers, name="update-workers"),
    path("worker-details/<int:pk>/", worker_details, name="worker-details"),
    path("delete-workers/<int:pk>/", delete_workers, name="delete-workers"),
    path("worker-attendance-form/", worker_attendance, name="worker-attendance-form"),
    path("attendance-list/", attendance_list, name="attendance-list"),
    path("update-attendance/<int:pk>/", update_attendance, name="update-attendance"),

    # API URLS
    path("api/workers/", WorkerListAPIView.as_view(), name="workers"),
    path("api/workers/<int:pk>/", WorkerDetailAPIView.as_view(), name="workers"),
    path("api/workers/<int:pk>/update/",WorkerUpdateAPIView.as_view(), name="worker-update"),
    path("api/workers/create/", WorkerCreateAPIView.as_view(), name="worker-create"),
    path('api/register/', RegisterWorkerAPIView.as_view(), name='user-register'),
]