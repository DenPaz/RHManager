from django import forms

from .models import (
    Policial,
    PolicialDadosPessoais,
    PolicialDadosProfissionais,
    PolicialFormacaoComplementar,
    PolicialTrabalhoAnterior,
)


class PolicialForm(forms.ModelForm):
    class Meta:
        model = Policial
        fields = (
            "matricula",
            "nome",
            "sobrenome",
            "cpf",
            "genero",
        )


class PolicialDadosPessoaisForm(forms.ModelForm):
    class Meta:
        model = PolicialDadosPessoais
        fields = (
            "nome_guerra",
            "data_nascimento",
            "tipo_sanguineo",
            "celular",
            "email",
            "endereco_logradouro",
            "endereco_numero",
            "endereco_bairro",
            "endereco_cidade",
            "endereco_estado",
            "endereco_cep",
        )
        widgets = {
            "data_nascimento": forms.DateInput(
                attrs={
                    "class": "form-control datepicker_input",
                }
            ),
        }


class PolicialDadosProfissionaisForm(forms.ModelForm):
    class Meta:
        model = PolicialDadosProfissionais
        fields = (
            "data_ingresso",
            "formacao_academica",
            "antiguidade",
            "lotacao_regiao",
            "lotacao_batalhao",
            "lotacao_companhia",
            "lotacao_pelotao",
            "lotacao_grupo",
            "lotacao_cidade",
            "comportamento",
            "proximas_ferias",
            "licencas_especiais_acumuladas",
            "afastamento",
            "afastamento_data_inicio",
            "afastamento_data_fim",
            "restricao",
            "restricao_data_fim",
            "observacoes",
        )
        widgets = {
            "data_ingresso": forms.DateInput(
                attrs={
                    "class": "form-control datepicker_input",
                }
            ),
            "formacao_academica": forms.SelectMultiple(
                attrs={
                    "class": "select2",
                    "id": "states",
                    "data-placeholder": "Selecione uma ou mais formações acadêmicas",
                    "name": "states[]",
                }
            ),
        }


class PolicialFormacaoComplementarForm(forms.ModelForm):
    class Meta:
        model = PolicialFormacaoComplementar
        fields = (
            "cursos",
            "cursos_pm",
            "cursos_civis",
            "linguas_estrangeiras",
        )


class PolicialTrabalhoAnteriorForm(forms.ModelForm):
    class Meta:
        model = PolicialTrabalhoAnterior
        fields = (
            "tipo",
            "tempo",
        )
