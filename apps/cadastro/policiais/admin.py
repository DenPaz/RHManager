from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Policial,
    PolicialDadosPessoais,
    PolicialDadosProfissionais,
    PolicialFormacaoComplementar,
    PolicialTrabalhoAnterior,
)
from .resources import PolicialResource


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


admin.site.register(PolicialDadosPessoais)
admin.site.register(PolicialFormacaoComplementar)
# admin.site.register(PolicialDadosProfissionais)
admin.site.register(PolicialTrabalhoAnterior)


@admin.register(PolicialDadosProfissionais)
class PolicialDadosProfissionaisAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "data_aposentadoria",
    )
