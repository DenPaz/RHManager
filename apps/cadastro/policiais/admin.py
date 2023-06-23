from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    DadosPessoais,
    DadosProfissionais,
    FormacaoComplementar,
    RegistroInicial,
    TrabalhoAnterior,
)
from .resources import PolicialResource


@admin.register(RegistroInicial)
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


admin.site.register(DadosPessoais)
admin.site.register(FormacaoComplementar)
# admin.site.register(DadosProfissionais)
admin.site.register(TrabalhoAnterior)


@admin.register(DadosProfissionais)
class PolicialDadosProfissionaisAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "aposentadoria",
    )
