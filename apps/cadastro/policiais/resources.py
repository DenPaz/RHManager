from django.core.exceptions import ValidationError
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
        exclude = ("id", "created", "modified")
        import_id_fields = ["matricula"]
        clean_model_instances = True
        skip_unchanged = True


class PolicialForeignKeyResource(PolicialBaseResource):
    policial = fields.Field(
        column_name="matricula",
        attribute="policial",
        widget=ForeignKeyWidget(Policial, "matricula"),
    )

    class Meta(PolicialBaseResource.Meta):
        import_id_fields = ["policial"]


class PolicialResource(PolicialBaseResource):
    class Meta:
        model = Policial


class PolicialDadosPessoaisResource(PolicialForeignKeyResource):
    class Meta:
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
        widget=ForeignKeyWidget(PolicialTrabalhoAnterior, "label"),
    )
    restricao = fields.Field(
        column_name="restricao",
        attribute="restricao",
        widget=ForeignKeyWidget(PolicialTrabalhoAnterior, "label"),
    )

    class Meta:
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

    class Meta:
        model = PolicialFormacaoComplementar


class PolicialTrabalhoAnteriorResource(PolicialForeignKeyResource):
    class Meta:
        model = PolicialTrabalhoAnterior
        import_id_fields = ["tipo"]
