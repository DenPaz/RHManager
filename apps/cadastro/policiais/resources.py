from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import (
    Policial,
    PolicialDadosPessoais,
    PolicialDadosProfissionais,
    PolicialFormacaoComplementar,
    PolicialTrabalhoAnterior,
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
        widget=ManyToManyWidget(PolicialFormacaoComplementar, field="label"),
    )
    afastamento = fields.Field(
        column_name="afastamento",
        attribute="afastamento",
        widget=ForeignKeyWidget(PolicialTrabalhoAnterior, field="label"),
    )
    restricao = fields.Field(
        column_name="restricao",
        attribute="restricao",
        widget=ForeignKeyWidget(PolicialTrabalhoAnterior, field="label"),
    )

    class Meta(PolicialForeignKeyResource.Meta):
        model = PolicialDadosProfissionais


class PolicialFormacaoComplementarResource(PolicialForeignKeyResource):
    cursos = fields.Field(
        column_name="cursos",
        attribute="cursos",
        widget=ManyToManyWidget(PolicialFormacaoComplementar, field="label"),
    )
    cursos_pm = fields.Field(
        column_name="cursos_pm",
        attribute="cursos_pm",
        widget=ManyToManyWidget(PolicialFormacaoComplementar, field="label"),
    )
    cursos_civis = fields.Field(
        column_name="cursos_civis",
        attribute="cursos_civis",
        widget=ManyToManyWidget(PolicialFormacaoComplementar, field="label"),
    )
    linguas_estrangeiras = fields.Field(
        column_name="linguas_estrangeiras",
        attribute="linguas_estrangeiras",
        widget=ManyToManyWidget(PolicialFormacaoComplementar, field="label"),
    )

    class Meta(PolicialForeignKeyResource.Meta):
        model = PolicialFormacaoComplementar


class PolicialTrabalhoAnteriorResource(PolicialForeignKeyResource):
    class Meta(PolicialForeignKeyResource.Meta):
        model = PolicialTrabalhoAnterior
        import_id_fields = ["tipo"]
