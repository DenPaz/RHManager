from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Policial,
    PolicialDadosPessoais,
    PolicialDadosProfissionais,
    PolicialFormacaoComplementar,
    PolicialTrabalhoAnterior,
)
from .resources import (
    PolicialDadosPessoaisResource,
    PolicialDadosProfissionaisResource,
    PolicialFormacaoComplementarResource,
    PolicialResource,
    PolicialTrabalhoAnteriorResource,
)


@admin.register(Policial)
class PolicialAdmin(ImportExportModelAdmin):
    list_display = (
        "matricula",
        "nome",
        "sobrenome",
        "cpf_formatado",
        "genero",
    )
    list_filter = ("genero",)
    search_fields = (
        "matricula",
        "nome",
        "sobrenome",
        "cpf",
    )
    readonly_fields = (
        "created",
        "modified",
    )
    ordering = (
        "nome",
        "sobrenome",
    )
    list_per_page = 10
    resource_class = PolicialResource


class PolicialBaseAdmin(ImportExportModelAdmin):
    list_filter = ("policial__genero",)
    search_fields = (
        "policial__matricula",
        "policial__nome",
        "policial__sobrenome",
        "policial__cpf",
    )
    readonly_fields = (
        "created",
        "modified",
    )
    ordering = ("policial",)
    list_per_page = 10


@admin.register(PolicialDadosPessoais)
class PolicialDadosPessoaisAdmin(PolicialBaseAdmin):
    list_display = (
        "policial",
        "nome_guerra",
        "data_nascimento",
        "tipo_sanguineo",
        "email",
        "celular_formatado",
        "endereco",
    )
    resource_class = PolicialDadosPessoaisResource


@admin.register(PolicialDadosProfissionais)
class PolicialDadosProfissionaisAdmin(PolicialBaseAdmin):
    list_display = (
        "policial",
        "data_ingresso",
        "data_aposentadoria",
        "proximas_ferias",
        "antiguidade",
        "comportamento",
        "afastamento",
        "afastamento_data_inicio",
        "afastamento_data_fim",
        "restricao",
        "restricao_data_fim",
        "lotacao",
    )
    resource_class = PolicialDadosProfissionaisResource


@admin.register(PolicialFormacaoComplementar)
class PolicialFormacaoComplementarAdmin(PolicialBaseAdmin):
    list_display = ("policial",)
    resource_class = PolicialFormacaoComplementarResource


@admin.register(PolicialTrabalhoAnterior)
class PolicialTrabalhoAnteriorAdmin(PolicialBaseAdmin):
    list_display = (
        "policial",
        "tipo",
        "tempo",
    )
    resource_class = PolicialTrabalhoAnteriorResource
