from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Afastamento,
    Curso,
    CursoCivil,
    CursoPM,
    FormacaoAcademica,
    LinguaEstrangeira,
    Restricao,
)
from .resources import (
    AfastamentoResource,
    CursoCivilResource,
    CursoPMResource,
    CursoResource,
    FormacaoAcademicaResource,
    LinguaEstrangeiraResource,
    RestricaoResource,
)


class DadoComplementarAdmin(ImportExportModelAdmin):
    list_display = ("__str__",)
    search_fields = ("label",)
    ordering = ("label",)
    list_per_page = 10
    resource_class = None

    class Meta:
        abstract = True


@admin.register(Afastamento)
class AfastamentoAdmin(DadoComplementarAdmin):
    resource_class = AfastamentoResource


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


@admin.register(Restricao)
class RestricaoAdmin(DadoComplementarAdmin):
    resource_class = RestricaoResource
