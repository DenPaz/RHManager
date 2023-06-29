from django.core.exceptions import ValidationError
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

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
        skip_unchanged = True
        clean_model_instances = True


class PolicialResource(PolicialBaseResource):
    class Meta:
        model = Policial
        import_id_fields = ["matricula"]


class PolicialForeignKeyResource(PolicialBaseResource):
    policial = fields.Field(
        column_name="matricula",
        attribute="policial",
        widget=ForeignKeyWidget(Policial, "matricula"),
    )

    class Meta:
        import_id_fields = ["policial"]

    def before_import_row(self, row, **kwargs):
        matricula = row.get("matricula")
        if not Policial.objects.filter(matricula=matricula).exists():
            raise ValidationError(f"Policial com matrícula {matricula} não existe.")


class PolicialDadosPessoaisResource(PolicialForeignKeyResource):
    class Meta:
        model = PolicialDadosPessoais


class PolicialDadosProfissionaisResource(PolicialForeignKeyResource):
    class Meta:
        model = PolicialDadosProfissionais


class PolicialFormacaoComplementarResource(PolicialForeignKeyResource):
    class Meta:
        model = PolicialFormacaoComplementar


class PolicialTrabalhoAnteriorResource(PolicialForeignKeyResource):
    class Meta:
        model = PolicialTrabalhoAnterior
