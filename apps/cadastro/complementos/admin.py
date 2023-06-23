from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Curso,
    CursoCivil,
    CursoPM,
    FormacaoAcademica,
    LinguaEstrangeira,
    TipoAfastamento,
    TipoRestricao,
)
from .resources import (
    CursoCivilResource,
    CursoPMResource,
    CursoResource,
    FormacaoAcademicaResource,
    LinguaEstrangeiraResource,
    TipoAfastamentoResource,
    TipoRestricaoResource,
)


class DadoComplementarAdmin(ImportExportModelAdmin):
    list_display = ("__str__",)
    search_fields = ("label",)
    ordering = ("label",)
    list_per_page = 10
    resource_class = None

    class Meta:
        abstract = True


@admin.register(TipoAfastamento)
class TipoAfastamentoAdmin(DadoComplementarAdmin):
    resource_class = TipoAfastamentoResource


@admin.register(Curso)
class CursoAdmin(DadoComplementarAdmin):
    resource_class = CursoResource


@admin.register(CursoCivil)
class CursoCivilAdmin(DadoComplementarAdmin):
    resource_class = CursoCivilResource


@admin.register(CursoPM)
class CursoPMAdmin(DadoComplementarAdmin):
    resource_class = CursoPMResource


@admin.register(FormacaoAcademica)
class FormacaoAcademicaAdmin(DadoComplementarAdmin):
    resource_class = FormacaoAcademicaResource


@admin.register(LinguaEstrangeira)
class LinguaEstrangeiraAdmin(DadoComplementarAdmin):
    resource_class = LinguaEstrangeiraResource


@admin.register(TipoRestricao)
class TipoRestricaoAdmin(DadoComplementarAdmin):
    resource_class = TipoRestricaoResource
