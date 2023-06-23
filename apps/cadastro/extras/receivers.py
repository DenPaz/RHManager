from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import (
    Afastamento,
    CursoCivil,
    CursoPM,
    FormacaoAcademica,
    LinguaEstrangeira,
    Restricao,
)

model_default_values = {
    LinguaEstrangeira: [
        "Inglês",
        "Espanhol",
        "Francês",
        "Italiano",
        "Alemão",
        "Mandarim",
        "Japonês",
        "Russo",
        "Árabe",
    ],
    CursoCivil: [
        "Administração",
        "Arquitetura",
    ],
}


@receiver(post_migrate)
def populate_default_values(sender, **kwargs):
    for model, values in model_default_values.items():
        for value in values:
            model.objects.get_or_create(label=value)
