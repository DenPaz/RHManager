from django.urls import path

from .views import (
    PoliciaisCreateView,
    PoliciaisListView,
    PoliciaisUpdateView,
    PolicialDeleteView,
    PolicialDetailView,
)

app_name = "policiais"

urlpatterns = [
    path(
        route="list/",
        view=PoliciaisListView.as_view(),
        name="list",
    ),
    path(
        route="create/",
        view=PoliciaisCreateView.as_view(),
        name="create",
    ),
    path(
        route="update/<str:pk>/",
        view=PoliciaisUpdateView.as_view(),
        name="update",
    ),
    path(
        route="delete/<str:pk>/",
        view=PolicialDeleteView.as_view(),
        name="delete",
    ),
    path(
        route="details/<str:pk>/",
        view=PolicialDetailView.as_view(),
        name="detail",
    ),
]
