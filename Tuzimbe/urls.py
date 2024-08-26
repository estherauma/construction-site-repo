from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import index, base, add_workers,all_workers,update_workers,worker_details,delete_workers,worker_attendance,attendance_list,update_attendance, add_material, all_materials, details, edit_material, material_usage, signup,logout_user
from .views import WorkerListAPIView, WorkerDetailAPIView, WorkerUpdateAPIView, WorkerCreateAPIView, RegisterWorkerAPIView, MaterialAllView, MaterialDetailview
from django.contrib.auth.views import LoginView
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
    path("add_workers/", add_workers, name="add_workers"),
    path("all_workers/", all_workers, name="all_workers"),
    path("update_workers/<int:pk>/", update_workers, name="update_workers"),
    path("worker_details/<int:pk>/", worker_details, name="worker_details"),
    path("delete_workers/<int:pk>/", delete_workers, name="delete_workers"),
    path("worker_attendance_form/", worker_attendance, name="worker_attendance_form"),
    path("attendance_list/", attendance_list, name="attendance_list"),
    path("update_attendance/<int:pk>/", update_attendance, name="update_attendance"),
    path('login/', LoginView.as_view(template_name ='auth/login.html'), name = 'login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_user, name = 'logout'),

    # API URLS
    path("api/workers/", WorkerListAPIView.as_view(), name="workers"),
    path("api/workers/<int:pk>/", WorkerDetailAPIView.as_view(), name="workers"),
    path("api/workers/<int:pk>/update/",WorkerUpdateAPIView.as_view(), name="worker_update"),
    path("api/workers/create/", WorkerCreateAPIView.as_view(), name="worker_create"),
    path('api/register/', RegisterWorkerAPIView.as_view(), name='user_register'),
]