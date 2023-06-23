from django.urls import path

from .views import CursoView

app_name = "complementos"

urlpatterns = [
    path(
        route="curso/",
        view=CursoView.as_view(),
        name="curso",
    ),
]
