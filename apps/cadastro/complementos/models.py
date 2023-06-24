from django.db import models
from model_utils.fields import UUIDField

from ..utils import get_capitalized_words


class DadoComplementar(models.Model):
    id = UUIDField(
        primary_key=True,
        editable=False,
        version=4,
    )
    label = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Descrição",
    )

    class Meta:
        abstract = True
        ordering = ["label"]

    def __str__(self):
        return f"{self.label}"

    def clean(self):
        super().clean()
        self.label = get_capitalized_words(self.label)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class FormacaoAcademica(DadoComplementar):
    class Meta:
        verbose_name = "Formação acadêmica"
        verbose_name_plural = "Formação acadêmica"


class Curso(DadoComplementar):
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"


class CursoPM(DadoComplementar):
    class Meta:
        verbose_name = "Curso da PM"
        verbose_name_plural = "Cursos da PM"


class CursoCivil(DadoComplementar):
    class Meta:
        verbose_name = "Curso civil"
        verbose_name_plural = "Cursos civis"


class LinguaEstrangeira(DadoComplementar):
    class Meta:
        verbose_name = "Língua estrangeira"
        verbose_name_plural = "Línguas estrangeiras"


class TipoAfastamento(DadoComplementar):
    class Meta:
        verbose_name = "Tipo de afastamento"
        verbose_name_plural = "Tipos de afastamentos"


class TipoRestricao(DadoComplementar):
    class Meta:
        verbose_name = "Tipo de restrição"
        verbose_name_plural = "Tipos de restrições"
