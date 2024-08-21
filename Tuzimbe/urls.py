from django.urls import path, include
from .views import index, base, add_workers,all_workers,update_workers,worker_details

app_name = "Tuzimbe"

urlpatterns = [
    path("", index, name="index"),
    path("base", base, name="base"),
    path("add-workers/", add_workers, name="add-workers"),
    path("all-workers/", all_workers, name="all-workers"),
    path("update-workers/<int:pk>/", update_workers, name="update-workers"),
    path("worker-details/<int:pk>/", worker_details, name="worker-details")
]