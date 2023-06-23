from import_export import resources

from ..utils import get_capitalized_words
from .models import (
    Curso,
    CursoCivil,
    CursoPM,
    FormacaoAcademica,
    LinguaEstrangeira,
    TipoAfastamento,
    TipoRestricao,
)


class DadoComplementarResource(resources.ModelResource):
    class Meta:
        abstract = True
        exclude = ("id",)
        import_id_fields = ["label"]
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, **kwargs):
        row["label"] = get_capitalized_words(row["label"])
        if self._meta.model.objects.filter(**row).exists():
            kwargs["skip_row"] = True


class TipoAfastamentoResource(DadoComplementarResource):
    class Meta(DadoComplementarResource.Meta):
        model = TipoAfastamento


class CursoResource(DadoComplementarResource):
    class Meta(DadoComplementarResource.Meta):
        model = Curso


class CursoCivilResource(DadoComplementarResource):
    class Meta(DadoComplementarResource.Meta):
        model = CursoCivil


class CursoPMResource(DadoComplementarResource):
    class Meta(DadoComplementarResource.Meta):
        model = CursoPM


class FormacaoAcademicaResource(DadoComplementarResource):
    class Meta(DadoComplementarResource.Meta):
        model = FormacaoAcademica


class LinguaEstrangeiraResource(DadoComplementarResource):
    class Meta(DadoComplementarResource.Meta):
        model = LinguaEstrangeira


class TipoRestricaoResource(DadoComplementarResource):
    class Meta(DadoComplementarResource.Meta):
        model = TipoRestricao
