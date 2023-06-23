from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    DadosPessoais,
    DadosProfissionais,
    FormacaoComplementar,
    Registro,
    TrabalhoAnterior,
)
from .resources import RegistroResource


@admin.register(Registro)
class RegistroAdmin(ImportExportModelAdmin):
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
    resource_class = RegistroResource


admin.site.register(DadosPessoais)
admin.site.register(FormacaoComplementar)
# admin.site.register(DadosProfissionais)
admin.site.register(TrabalhoAnterior)


@admin.register(DadosProfissionais)
class DadosProfissionaisAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "aposentadoria",
    )
