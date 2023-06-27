from django.urls import path

from .views import ComplementosListView

app_name = "complementos"

urlpatterns = [
    path(
        route="list/",
        view=ComplementosListView.as_view(),
        name="list",
    ),
]
