from django.urls import path

from .views import LoginView, LogoutView

app_name = "authentication"

urlpatterns = [
    path(
        route="login/",
        view=LoginView.as_view(),
        name="login",
    ),
    path(
        route="logout/",
        view=LogoutView.as_view(),
        name="logout",
    ),
]
