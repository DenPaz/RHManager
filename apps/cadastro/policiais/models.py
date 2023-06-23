from datetime import date

from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from model_utils.fields import UUIDField
from model_utils.models import TimeStampedModel

from ..constants import (
    Comportamento,
    Estado,
    Genero,
    TipoSanguineo,
    TipoTrabalhoAnterior,
)
from ..extras.models import (
    Afastamento,
    Curso,
    CursoCivil,
    CursoPM,
    FormacaoAcademica,
    LinguaEstrangeira,
    Restricao,
)
from ..utils import get_capitalized_words
from ..validators import ValidateFillZeros, ValidateOnlyNumbers


class Registro(TimeStampedModel):
    id = UUIDField(
        primary_key=True,
        editable=False,
        version=4,
    )
    matricula = models.CharField(
        unique=True,
        max_length=6,
        validators=[ValidateOnlyNumbers(6)],
        verbose_name="Matrícula",
        help_text="Somente números (6 dígitos)",
    )
    nome = models.CharField(
        max_length=50,
        verbose_name="Nome",
    )
    sobrenome = models.CharField(
        max_length=50,
        verbose_name="Sobrenome",
    )
    cpf = models.CharField(
        unique=True,
        max_length=11,
        validators=[ValidateOnlyNumbers(11)],
        verbose_name="CPF",
        help_text="Somente números (11 dígitos)",
    )
    genero = models.CharField(
        max_length=1,
        choices=Genero.choices,
        verbose_name="Gênero",
    )

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"
        ordering = ["nome", "sobrenome"]

    def __str__(self):
        return f"{self.nome} {self.sobrenome} ({self.matricula})"

    def save(self, *args, **kwargs):
        self.full_clean()
        self.nome = get_capitalized_words(self.nome)
        self.sobrenome = get_capitalized_words(self.sobrenome)
        super().save(*args, **kwargs)

    @property
    def nome_completo(self):
        return f"{self.nome} {self.sobrenome}"

    @property
    def cpf_formatado(self):
        return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"


class DadosPessoais(TimeStampedModel):
    policial = models.OneToOneField(
        Registro,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Policial",
    )
    nome_guerra = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Nome de guerra",
    )
    data_nascimento = models.DateField(
        verbose_name="Data de nascimento",
    )
    tipo_sanguineo = models.CharField(
        max_length=3,
        choices=TipoSanguineo.choices,
        verbose_name="Tipo sanguíneo",
    )
    celular = models.CharField(
        max_length=11,
        validators=[ValidateOnlyNumbers(11)],
        blank=True,
        verbose_name="Número de celular",
        help_text="Somente números (11 dígitos)",
    )
    email = models.EmailField(
        verbose_name="E-mail",
        blank=True,
    )
    endereco_logradouro = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Logradouro",
    )
    endereco_numero = models.CharField(
        max_length=5,
        blank=True,
        verbose_name="Número",
    )
    endereco_bairro = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Bairro",
    )
    endereco_cidade = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Cidade",
    )
    endereco_estado = models.CharField(
        max_length=2,
        choices=Estado.choices,
        blank=True,
        verbose_name="Estado",
    )
    endereco_cep = models.CharField(
        max_length=8,
        validators=[ValidateOnlyNumbers(8)],
        blank=True,
        verbose_name="CEP",
        help_text="Somente números (8 dígitos)",
    )

    class Meta:
        verbose_name = "Dados Pessoais"
        verbose_name_plural = "Dados Pessoais"
        ordering = ["policial__nome", "policial__sobrenome"]

    def __str__(self):
        return f"{self.policial.__str__()}"

    def save(self, *args, **kwargs):
        self.full_clean()
        self.nome_guerra = get_capitalized_words(self.nome_guerra)
        self.endereco_logradouro = get_capitalized_words(self.endereco_logradouro)
        self.endereco_bairro = get_capitalized_words(self.endereco_bairro)
        self.endereco_cidade = get_capitalized_words(self.endereco_cidade)
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    @property
    def idade(self):
        return relativedelta(timezone.now(), self.data_nascimento).years

    @property
    def celular_formatado(self):
        if self.celular:
            return f"({self.celular[:2]}) {self.celular[2:7]}-{self.celular[7:]}"
        return None

    @property
    def endereco(self):
        params = [
            self.endereco_logradouro,
            self.endereco_numero,
            self.endereco_bairro,
            self.endereco_cidade,
            self.endereco_estado,
            self.endereco_cep,
        ]
        return ", ".join([param for param in params if param])


class DadosProfissionais(TimeStampedModel):
    policial = models.OneToOneField(
        Registro,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Policial",
    )
    formacao_academica = models.ManyToManyField(
        FormacaoAcademica,
        blank=True,
        verbose_name="Formação acadêmica",
    )
    data_ingresso = models.DateField(
        verbose_name="Data de ingresso",
    )
    antiguidade = models.CharField(
        max_length=5,
        validators=[ValidateFillZeros(5)],
        verbose_name="Ordem de antiguidade",
        help_text="Somente números",
    )
    lotacao_regiao = models.CharField(
        max_length=2,
        validators=[ValidateOnlyNumbers(2)],
        verbose_name="Lotação: Região",
        help_text="Somente números (2 dígitos)",
    )
    lotacao_batalhao = models.CharField(
        max_length=2,
        validators=[ValidateOnlyNumbers(2)],
        verbose_name="Lotação: Batalhão",
        help_text="Somente números (2 dígitos)",
    )
    lotacao_companhia = models.CharField(
        max_length=2,
        validators=[ValidateOnlyNumbers(2)],
        verbose_name="Lotação: Companhia",
        help_text="Somente números (2 dígitos)",
    )
    lotacao_pelotao = models.CharField(
        max_length=2,
        validators=[ValidateOnlyNumbers(2)],
        verbose_name="Lotação: Pelotão",
        help_text="Somente números (2 dígitos)",
    )
    lotacao_grupo = models.CharField(
        max_length=1,
        validators=[ValidateOnlyNumbers(1)],
        verbose_name="Lotação: Grupo",
        help_text="Somente números (1 dígito)",
    )
    lotacao_cidade = models.CharField(
        max_length=50,
        verbose_name="Lotação: Cidade",
    )
    comportamento = models.CharField(
        max_length=11,
        choices=Comportamento.choices,
        verbose_name="Comportamento",
    )
    proximas_ferias = models.DateField(
        null=True,
        blank=True,
        verbose_name="Próximas férias",
    )
    licencas_especiais_acumuladas = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Licenças especiais acumuladas",
    )
    afastamento = models.ForeignKey(
        Afastamento,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Tipo de afastamento",
    )
    afastamento_data_inicio = models.DateField(
        blank=True,
        null=True,
        verbose_name="Início do afastamento",
    )
    afastamento_data_fim = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fim do afastamento",
    )
    restricao = models.ForeignKey(
        Restricao,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Tipo de restrição",
    )
    restricao_data_fim = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fim da restrição",
    )
    observacoes = models.TextField(
        blank=True,
        verbose_name="Observações",
    )

    class Meta:
        verbose_name = "Dados Profissionais"
        verbose_name_plural = "Dados Profissionais"
        ordering = ["policial__nome", "policial__sobrenome"]

    def __str__(self):
        return f"{self.policial.__str__()}"

    def save(self, *args, **kwargs):
        self.full_clean()
        self.lotacao_cidade = get_capitalized_words(self.lotacao_cidade)
        super().save(*args, **kwargs)

    @property
    def lotacao(self):
        params = [
            self.lotacao_regiao,
            self.lotacao_batalhao,
            self.lotacao_companhia,
            self.lotacao_pelotao,
            self.lotacao_grupo,
            self.lotacao_cidade,
        ]
        return "-".join([param for param in params if param])

    @property
    def tempo_proximas_ferias(self):
        return relativedelta(self.proximas_ferias, timezone.now().date())

    @property
    def tempo_afastamento(self):
        if self.afastamento_data_inicio and self.afastamento_data_fim:
            return relativedelta(
                self.afastamento_data_fim, self.afastamento_data_inicio
            )

    @property
    def tempo_restricao(self):
        if self.restricao_data_fim:
            return relativedelta(self.restricao_data_fim, timezone.now().date())

    @property
    def tempo_servico(self):
        return relativedelta(timezone.now().date(), self.data_ingresso)

    @property
    def aposentadoria(self):
        data_hoje = timezone.now().date()
        data_ingresso = self.data_ingresso

        if data_ingresso >= date(2022, 1, 1):
            for trabalho_anterior in self.policial.trabalhoanterior_set.all():
                if trabalho_anterior.label == TipoTrabalhoAnterior.NENHUM:
                    return data_ingresso + relativedelta(years=35)


class TrabalhoAnterior(models.Model):
    policial = models.ForeignKey(
        Registro,
        on_delete=models.CASCADE,
        verbose_name="Policial",
    )
    label = models.CharField(
        max_length=50,
        choices=TipoTrabalhoAnterior.choices,
        default=TipoTrabalhoAnterior.NENHUM,
        verbose_name="Tipo de trabalho anterior",
    )
    tempo = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Tempo de serviço no trabalho anterior (em dias)",
    )

    class Meta:
        verbose_name = "Trabalho Anterior"
        verbose_name_plural = "Trabalhos Anteriores"
        ordering = ["policial__nome", "policial__sobrenome"]
        unique_together = ("label", "policial")

    def __str__(self):
        return (
            f"{self.policial.__str__()}: {self.get_label_display()} ({self.tempo} dias)"
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.label == TipoTrabalhoAnterior.NENHUM:
            self.tempo = 0
        super().save(*args, **kwargs)


class FormacaoComplementar(TimeStampedModel):
    policial = models.OneToOneField(
        Registro,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Policial",
    )
    cursos = models.ManyToManyField(
        Curso,
        blank=True,
        verbose_name="Cursos",
    )
    cursos_pm = models.ManyToManyField(
        CursoPM,
        blank=True,
        verbose_name="Cursos da PM",
    )
    cursos_civis = models.ManyToManyField(
        CursoCivil,
        blank=True,
        verbose_name="Cursos Civis",
    )
    linguas_estrangeiras = models.ManyToManyField(
        LinguaEstrangeira,
        blank=True,
        verbose_name="Línguas Estrangeiras",
    )

    class Meta:
        verbose_name = "Formação Complementar"
        verbose_name_plural = "Formações Complementar"
        ordering = ["policial__nome", "policial__sobrenome"]

    def __str__(self):
        return f"{self.policial.__str__()}"
