from django.apps import AppConfig


class ExtrasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cadastro.extras"
    verbose_name = "Cadastro: Extras"

    def ready(self):
        import apps.cadastro.extras.receivers
