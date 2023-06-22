from django.urls import include, path

app_name = "cadastro"

urlpatterns = [
    path("policiais/", include("apps.cadastro.policiais.urls", namespace="policiais")),
    path("extras/", include("apps.cadastro.extras.urls", namespace="extras")),
]
