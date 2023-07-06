from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import (
    Curso,
    CursoCivil,
    CursoPM,
    FormacaoAcademica,
    LinguaEstrangeira,
    Policial,
    PolicialDadosPessoais,
    PolicialDadosProfissionais,
    PolicialFormacaoComplementar,
    PolicialTrabalhoAnterior,
    TipoAfastamento,
    TipoRestricao,
)


class PolicialBaseResource(resources.ModelResource):
    class Meta:
        import_id_fields = ["matricula"]
        exclude = ("id", "created", "modified")
        clean_model_instances = True
        skip_unchanged = True


class PolicialForeignKeyResource(PolicialBaseResource):
    policial = fields.Field(
        column_name="matricula",
        attribute="policial",
        widget=ForeignKeyWidget(Policial, field="matricula"),
    )

    class Meta(PolicialBaseResource.Meta):
        import_id_fields = ["policial"]


class PolicialResource(PolicialBaseResource):
    class Meta(PolicialBaseResource.Meta):
        model = Policial


class PolicialDadosPessoaisResource(PolicialForeignKeyResource):
    class Meta(PolicialForeignKeyResource.Meta):
        model = PolicialDadosPessoais


class PolicialDadosProfissionaisResource(PolicialForeignKeyResource):
    formacao_academica = fields.Field(
        column_name="formacao_academica",
        attribute="formacao_academica",
        widget=ManyToManyWidget(FormacaoAcademica, field="label"),
    )
    afastamento = fields.Field(
        column_name="afastamento",
        attribute="afastamento",
        widget=ForeignKeyWidget(TipoAfastamento, field="label"),
    )
    restricao = fields.Field(
        column_name="restricao",
        attribute="restricao",
        widget=ForeignKeyWidget(TipoRestricao, field="label"),
    )

    class Meta(PolicialForeignKeyResource.Meta):
        model = PolicialDadosProfissionais


class PolicialFormacaoComplementarResource(PolicialForeignKeyResource):
    cursos = fields.Field(
        column_name="cursos",
        attribute="cursos",
        widget=ManyToManyWidget(Curso, field="label"),
    )
    cursos_pm = fields.Field(
        column_name="cursos_pm",
        attribute="cursos_pm",
        widget=ManyToManyWidget(CursoPM, field="label"),
    )
    cursos_civis = fields.Field(
        column_name="cursos_civis",
        attribute="cursos_civis",
        widget=ManyToManyWidget(CursoCivil, field="label"),
    )
    linguas_estrangeiras = fields.Field(
        column_name="linguas_estrangeiras",
        attribute="linguas_estrangeiras",
        widget=ManyToManyWidget(LinguaEstrangeira, field="label"),
    )

    class Meta(PolicialForeignKeyResource.Meta):
        model = PolicialFormacaoComplementar


class PolicialTrabalhoAnteriorResource(PolicialForeignKeyResource):
    class Meta(PolicialForeignKeyResource.Meta):
        model = PolicialTrabalhoAnterior
        import_id_fields = ["tipo"]


# this class is used to import data from all the models
# class PolicialMixedResource(resources.ModelResource):
#     class Meta:
#         model = Policial
#         import_id_fields = ["matricula"]
#         exclude = ("id", "created", "modified")
#         clean_model_instances = True
#         skip_unchanged = True

#     def before_import_row(self, row, **kwargs):
#         row["policialdadospessoais_set-0-policial"] = row["matricula"]
#         row["policialdadosprofissionais_set-0-policial"] = row["matricula"]
#         row["policialformacaocomplementar_set-0-policial"] = row["matricula"]
#         row["policialtrabalhoanterior_set-0-policial"] = row["matricula"]
