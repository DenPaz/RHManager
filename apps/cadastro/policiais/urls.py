from django.urls import path

from .views import PoliciaisListView

app_name = "policiais"

urlpatterns = [
    path(
        route="list/",
        view=PoliciaisListView.as_view(),
        name="list",
    ),
]
