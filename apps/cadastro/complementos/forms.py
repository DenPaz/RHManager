from django import forms

from ..utils import get_capitalized_words
from .models import (
    Curso,
    CursoCivil,
    CursoPM,
    FormacaoAcademica,
    LinguaEstrangeira,
    TipoAfastamento,
    TipoRestricao,
)

# class DadoComplementarForm(forms.ModelForm):
#     label = forms.CharField(
#         label="Nome",
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#     )

#     class Meta:
#         fields = ["label"]

#     def clean(self):
#         super().clean()
#         self.cleaned_data["label"] = get_capitalized_words(self.cleaned_data["label"])

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)


# class CursoForm(DadoComplementarForm):
#     class Meta:
#         model = Curso
