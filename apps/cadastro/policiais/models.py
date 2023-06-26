from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from model_utils.fields import UUIDField
from model_utils.models import TimeStampedModel

from ..complementos.models import (
    Curso,
    CursoCivil,
    CursoPM,
    FormacaoAcademica,
    LinguaEstrangeira,
    TipoAfastamento,
    TipoRestricao,
)
from ..constants import (
    Comportamento,
    Estado,
    Genero,
    TipoSanguineo,
    TipoTrabalhoAnterior,
)
from ..utils import get_capitalized_words
from ..validators import ValidateFillZeros, ValidateOnlyNumbers


class RegistroInicial(TimeStampedModel):
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
        verbose_name = "Registro inicial"
        verbose_name_plural = "Registros iniciais"
        ordering = ["nome", "sobrenome"]

    def __str__(self):
        return f"{self.nome} {self.sobrenome} ({self.matricula})"

    def clean(self):
        super().clean()
        self.nome = get_capitalized_words(self.nome)
        self.sobrenome = get_capitalized_words(self.sobrenome)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def nome_completo(self):
        return f"{self.nome} {self.sobrenome}"

    @property
    def cpf_formatado(self):
        return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"


class DadosPessoais(TimeStampedModel):
    policial = models.OneToOneField(
        RegistroInicial,
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
        verbose_name = "Dados pessoais"
        verbose_name_plural = "Dados pessoais"
        ordering = ["policial__nome", "policial__sobrenome"]

    def __str__(self):
        return f"{self.policial.__str__()}"

    def clean(self):
        super().clean()
        self.nome_guerra = get_capitalized_words(self.nome_guerra)
        self.endereco_logradouro = get_capitalized_words(self.endereco_logradouro)
        self.endereco_bairro = get_capitalized_words(self.endereco_bairro)
        self.endereco_cidade = get_capitalized_words(self.endereco_cidade)
        self.email = self.email.lower()

    def save(self, *args, **kwargs):
        self.full_clean()
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
        RegistroInicial,
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
        TipoAfastamento,
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
        TipoRestricao,
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
        verbose_name = "Dados profissionais"
        verbose_name_plural = "Dados profissionais"
        ordering = ["policial__nome", "policial__sobrenome"]

    def __str__(self):
        return f"{self.policial.__str__()}"

    def clean(self):
        super().clean()
        self.lotacao_cidade = get_capitalized_words(self.lotacao_cidade)

    def save(self, *args, **kwargs):
        self.full_clean()
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
            return relativedelta(self.afastamento_data_fim, self.afastamento_data_inicio)

    @property
    def tempo_restricao(self):
        if self.restricao_data_fim:
            return relativedelta(self.restricao_data_fim, timezone.now().date())

    @property
    def tempo_servico(self):
        return relativedelta(timezone.now().date(), self.data_ingresso)

    @property
    def tempo_trabalho_militar(self):
        tempo = relativedelta()
        trabalhos_anteriores = self.policial.trabalhoanterior_set.all()

        for trabalho_anterior in trabalhos_anteriores:
            if trabalho_anterior.tipo in (
                TipoTrabalhoAnterior.MILITAR_FEDERAL,
                TipoTrabalhoAnterior.PUBLICO_SC_MILITAR,
                TipoTrabalhoAnterior.PUBLICO_OUTRO_MILITAR,
            ):
                tempo += relativedelta(days=trabalho_anterior.tempo)

        return tempo

    @property
    def tempo_trabalho_nao_militar(self):
        tempo = relativedelta()
        trabalhos_anteriores = self.policial.trabalhoanterior_set.all()

        for trabalho_anterior in trabalhos_anteriores:
            if trabalho_anterior.tipo in (
                TipoTrabalhoAnterior.PRIVADO,
                TipoTrabalhoAnterior.PUBLICO_SC,
                TipoTrabalhoAnterior.PUBLICO_OUTRO,
            ):
                tempo += relativedelta(days=trabalho_anterior.tempo)

        return tempo

    @property
    def data_aposentadoria(self):
        pedagio = 0
        aposentadoria = None
        data_limite = date(2021, 12, 31)
        data_hoje = timezone.now().date()
        data_ingresso = self.data_ingresso
        policial_genero = self.policial.genero
        t_servico = self.tempo_servico
        t_trabalho_militar = self.tempo_trabalho_militar
        t_trabalho_nao_militar = self.tempo_trabalho_nao_militar
        t_trabalho_nao_militar_max = 5 * 365
        t_masculino = 30 * 365
        t_feminino = 25 * 365
        taxa = 0.17

        if data_ingresso <= data_limite:
            if policial_genero == Genero.MASCULINO:
                if not t_trabalho_militar and not t_trabalho_nao_militar:
                    pedagio += round((t_masculino - (data_limite - data_ingresso).days) * taxa)
                    aposentadoria = (
                        data_hoje
                        + relativedelta(years=30)
                        - t_servico
                        + relativedelta(days=pedagio)
                    )
                elif t_trabalho_nao_militar and not t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= (t_trabalho_nao_militar_max):
                        pedagio += round(
                            (
                                t_masculino
                                - (data_limite - data_ingresso).days
                                + t_trabalho_nao_militar_max
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=30)
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            + relativedelta(days=pedagio)
                        )
                    else:
                        pedagio += round(
                            (
                                t_masculino
                                - (data_limite - data_ingresso).days
                                + t_trabalho_nao_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=30)
                            - t_servico
                            - t_trabalho_nao_militar
                            + relativedelta(days=pedagio)
                        )
                elif t_trabalho_nao_militar and t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= (t_trabalho_nao_militar_max):
                        pedagio += round(
                            (
                                t_masculino
                                - (data_limite - data_ingresso).days
                                + t_trabalho_nao_militar_max
                                + t_trabalho_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=30)
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                    else:
                        pedagio += round(
                            (
                                t_masculino
                                - (data_limite - data_ingresso).days
                                + t_trabalho_nao_militar.days
                                + t_trabalho_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=30)
                            - t_servico
                            - t_trabalho_nao_militar
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                elif not t_trabalho_nao_militar and t_trabalho_militar:
                    pedagio += round(
                        (
                            t_masculino
                            - (data_limite - data_ingresso).days
                            + t_trabalho_militar.days
                        )
                        * taxa
                    )
                    aposentadoria = (
                        data_hoje
                        + relativedelta(years=30)
                        - t_servico
                        - t_trabalho_militar
                        + relativedelta(days=pedagio)
                    )
            elif policial_genero == Genero.FEMININO:
                if not t_trabalho_militar and not t_trabalho_nao_militar:
                    pedagio += round((t_feminino - (data_limite - data_ingresso).days) * taxa)
                    aposentadoria = (
                        data_hoje
                        + relativedelta(years=25)
                        - t_servico
                        + relativedelta(days=pedagio)
                    )
                elif t_trabalho_nao_militar and not t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= (t_trabalho_nao_militar_max):
                        pedagio += round(
                            (
                                t_feminino
                                - (data_limite - data_ingresso).days
                                + t_trabalho_nao_militar_max
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=25)
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            + relativedelta(days=pedagio)
                        )
                    else:
                        pedagio += round(
                            (
                                t_feminino
                                - (data_limite - data_ingresso).days
                                + t_trabalho_nao_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=25)
                            - t_servico
                            - t_trabalho_nao_militar
                            + relativedelta(days=pedagio)
                        )
                elif t_trabalho_nao_militar and t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= (t_trabalho_nao_militar_max):
                        pedagio += round(
                            (
                                t_feminino
                                - (data_limite - data_ingresso).days
                                + t_trabalho_nao_militar_max
                                + t_trabalho_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=25)
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                    else:
                        pedagio += round(
                            (
                                t_feminino
                                - (data_limite - data_ingresso).days
                                + t_trabalho_nao_militar.days
                                + t_trabalho_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=25)
                            - t_servico
                            - t_trabalho_nao_militar
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                elif not t_trabalho_nao_militar and t_trabalho_militar:
                    pedagio += round(
                        (t_feminino - (data_limite - data_ingresso).days + t_trabalho_militar.days)
                        * taxa
                    )
                    aposentadoria = (
                        data_hoje
                        + relativedelta(years=25)
                        - t_servico
                        - t_trabalho_militar
                        + relativedelta(days=pedagio)
                    )
        elif data_ingresso > data_limite:
            if policial_genero == Genero.MASCULINO:
                if not t_trabalho_militar and not t_trabalho_nao_militar:
                    aposentadoria = (
                        data_hoje
                        + relativedelta(years=30)
                        - t_servico
                        + relativedelta(days=pedagio)
                    )
                elif t_trabalho_nao_militar and not t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= (t_trabalho_nao_militar_max):
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=30)
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            + relativedelta(days=pedagio)
                        )
                    else:
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=30)
                            - t_servico
                            - t_trabalho_nao_militar
                            + relativedelta(days=pedagio)
                        )
                elif t_trabalho_nao_militar and t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= (t_trabalho_nao_militar_max):
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=30)
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                    else:
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=30)
                            - t_servico
                            - t_trabalho_nao_militar
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                elif not t_trabalho_nao_militar and t_trabalho_militar:
                    aposentadoria = (
                        data_hoje
                        + relativedelta(years=30)
                        - t_servico
                        - t_trabalho_militar
                        + relativedelta(days=pedagio)
                    )
            elif policial_genero == Genero.FEMININO:
                if not t_trabalho_militar and not t_trabalho_nao_militar:
                    aposentadoria = (
                        data_hoje
                        + relativedelta(years=25)
                        - t_servico
                        + relativedelta(days=pedagio)
                    )
                elif t_trabalho_nao_militar and not t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= (t_trabalho_nao_militar_max):
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=25)
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            + relativedelta(days=pedagio)
                        )
                    else:
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=25)
                            - t_servico
                            - t_trabalho_nao_militar
                            + relativedelta(days=pedagio)
                        )
                elif t_trabalho_nao_militar and t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= (t_trabalho_nao_militar_max):
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=25)
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                    else:
                        aposentadoria = (
                            data_hoje
                            + relativedelta(years=25)
                            - t_servico
                            - t_trabalho_nao_militar
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                elif not t_trabalho_nao_militar and t_trabalho_militar:
                    aposentadoria = (
                        data_hoje
                        + relativedelta(years=25)
                        - t_servico
                        - t_trabalho_militar
                        + relativedelta(days=pedagio)
                    )

        return aposentadoria


class TrabalhoAnterior(models.Model):
    policial = models.ForeignKey(
        RegistroInicial,
        on_delete=models.CASCADE,
        verbose_name="Policial",
    )
    tipo = models.CharField(
        max_length=50,
        choices=TipoTrabalhoAnterior.choices,
        default=TipoTrabalhoAnterior.NENHUM,
        verbose_name="Tipo de serviço anterior",
    )
    tempo = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Tempo de serviço anterior (dias)",
    )

    class Meta:
        verbose_name = "Trabalho anterior"
        verbose_name_plural = "Trabalhos anteriores"
        ordering = ["policial__nome", "policial__sobrenome"]
        unique_together = ("tipo", "policial")

    def __str__(self):
        return f"{self.policial.__str__()}: {self.get_tipo_display()} ({self.tempo} dias)"

    def clean(self):
        super().clean()
        if self.tipo == TipoTrabalhoAnterior.NENHUM:
            self.tempo = 0

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class FormacaoComplementar(TimeStampedModel):
    policial = models.OneToOneField(
        RegistroInicial,
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
        verbose_name = "Formação complementar"
        verbose_name_plural = "Formação complementar"
        ordering = ["policial__nome", "policial__sobrenome"]

    def __str__(self):
        return f"{self.policial.__str__()}"
