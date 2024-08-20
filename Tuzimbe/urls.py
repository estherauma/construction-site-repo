from django.urls import path, include
from .views import index, base, add_workers

app_name = "zimba"

urlpatterns = [
    path("", index, name="index"),
    path("base", base, name="base"),
    path("add-workers/", add_workers, name="add-workers"),
]