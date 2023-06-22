from django.db import models
from model_utils.fields import UUIDField

from ..utils import get_capitalized_words


class DadoComplementar(models.Model):
    id = UUIDField(
        primary_key=True,
        editable=False,
        version=4,
    )
    nome = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nome",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.nome}"

    def save(self, *args, **kwargs):
        self.nome = get_capitalized_words(self.nome)
        super().save(*args, **kwargs)


class FormacaoAcademica(DadoComplementar):
    class Meta:
        verbose_name = "Formação Acadêmica"
        verbose_name_plural = "Formações Acadêmicas"
        ordering = ["nome"]


class Curso(DadoComplementar):
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["nome"]


class CursoPM(DadoComplementar):
    class Meta:
        verbose_name = "Curso da PM"
        verbose_name_plural = "Cursos da PM"
        ordering = ["nome"]


class CursoCivil(DadoComplementar):
    class Meta:
        verbose_name = "Curso Civil"
        verbose_name_plural = "Cursos Civis"
        ordering = ["nome"]


class LinguaEstrangeira(DadoComplementar):
    class Meta:
        verbose_name = "Língua Estrangeira"
        verbose_name_plural = "Línguas Estrangeiras"
        ordering = ["nome"]


class TipoAfastamento(DadoComplementar):
    class Meta:
        verbose_name = "Tipo de Afastamento"
        verbose_name_plural = "Tipos de Afastamentos"
        ordering = ["nome"]


class TipoRestricao(DadoComplementar):
    class Meta:
        verbose_name = "Tipo de Restrição"
        verbose_name_plural = "Tipos de Restrições"
        ordering = ["nome"]
