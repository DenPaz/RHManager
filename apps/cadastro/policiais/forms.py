from django.forms import ModelForm, inlineformset_factory

from .models import (
    Policial,
    PolicialDadosPessoais,
    PolicialDadosProfissionais,
    PolicialFormacaoComplementar,
    PolicialTrabalhoAnterior,
)


class PolicialForm(ModelForm):
    class Meta:
        model = Policial
        fields = "__all__"
        exclude = ["id", "created_at", "updated_at"]


# PolicialDadosPessoaisFormSet = inlineformset_factory(
#     Policial,
#     PolicialDadosPessoais,
#     PolicialTrabalhoAnterior,
#     fields="__all__",
#     extra=1,
# )
