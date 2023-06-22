from django.urls import path

from .views import ExtraListView

app_name = "extras"

urlpatterns = [
    path(
        route="list/",
        view=ExtraListView.as_view(),
        name="list",
    ),
]
