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


@admin.register(PolicialDadosPessoais)
class PolicialDadosPessoaisAdmin(ImportExportModelAdmin):
    resource_class = PolicialDadosPessoaisResource
