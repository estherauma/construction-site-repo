from django.urls import path, include
from .views import index, base

app_name = "zimba"

urlpatterns = [
    path("", index, name="index"),
    path("base", base, name="base"),
]