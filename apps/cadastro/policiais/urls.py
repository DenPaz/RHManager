from django.urls import path

from .views import PolicialListView

app_name = "policiais"

urlpatterns = [
    path(
        route="list/",
        view=PolicialListView.as_view(),
        name="list",
    ),
]
