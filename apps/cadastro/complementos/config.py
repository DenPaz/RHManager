from django.apps import AppConfig


class ComplementosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cadastro.complementos"
    verbose_name = "Cadastro: Complementos"

    def ready(self):
        import apps.cadastro.complementos.receivers
