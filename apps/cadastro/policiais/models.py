from datetime import date

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
from ..validators import ValidateOnlyDigits


class Policial(TimeStampedModel):
    id = UUIDField(primary_key=True, editable=False)
    matricula = models.CharField(
        unique=True,
        max_length=6,
        validators=[ValidateOnlyDigits(6)],
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
        validators=[ValidateOnlyDigits(11)],
        verbose_name="CPF",
        help_text="Somente números (11 dígitos)",
    )
    genero = models.CharField(
        max_length=1,
        choices=Genero.choices,
        verbose_name="Gênero",
    )

    class Meta:
        verbose_name = "Policial"
        verbose_name_plural = "Policiais"
        ordering = ["nome", "sobrenome"]

    def __str__(self):
        return f"{self.nome_completo} ({self.matricula})"

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


class PolicialDadosPessoais(TimeStampedModel):
    id = UUIDField(primary_key=True, editable=False)
    policial = models.OneToOneField(
        Policial,
        on_delete=models.CASCADE,
        related_name="dados_pessoais",
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
        validators=[ValidateOnlyDigits(11)],
        blank=True,
        verbose_name="Número de celular",
        help_text="Somente números (11 dígitos)",
    )
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail",
    )
    endereco_logradouro = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Endereço - logradouro",
    )
    endereco_numero = models.CharField(
        max_length=5,
        blank=True,
        verbose_name="Endereço - número",
    )
    endereco_bairro = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Endereço - bairro",
    )
    endereco_cidade = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Endereço - cidade",
    )
    endereco_estado = models.CharField(
        max_length=2,
        choices=Estado.choices,
        blank=True,
        verbose_name="Endereço - estado",
    )
    endereco_cep = models.CharField(
        max_length=8,
        validators=[ValidateOnlyDigits(8)],
        blank=True,
        verbose_name="CEP",
        help_text="Somente números (8 dígitos)",
    )

    class Meta:
        verbose_name = "Policial: dados pessoais"
        verbose_name_plural = "Policiais: dados pessoais"
        ordering = ["policial__nome", "policial__sobrenome"]

    def __str__(self):
        return f"{self.policial.__str__()}"

    def clean(self):
        super().clean()
        self.email = self.email.lower()
        self.nome_guerra = get_capitalized_words(self.nome_guerra)
        self.endereco_logradouro = get_capitalized_words(self.endereco_logradouro)
        self.endereco_bairro = get_capitalized_words(self.endereco_bairro)
        self.endereco_cidade = get_capitalized_words(self.endereco_cidade)

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
        if any(params):
            return ", ".join([param for param in params if param])
        return None


class PolicialDadosProfissionais(TimeStampedModel):
    id = UUIDField(primary_key=True, editable=False)
    policial = models.OneToOneField(
        Policial,
        on_delete=models.CASCADE,
        related_name="dados_profissionais",
        verbose_name="Policial",
    )
    data_ingresso = models.DateField(
        verbose_name="Data de ingresso",
    )
    formacao_academica = models.ManyToManyField(
        FormacaoAcademica,
        blank=True,
        related_name="formacoes_academicas",
        verbose_name="Formação acadêmica",
    )
    antiguidade = models.CharField(
        max_length=5,
        validators=[ValidateOnlyDigits()],
        verbose_name="Ordem de antiguidade",
        help_text="Somente números",
    )
    lotacao_regiao = models.CharField(
        max_length=2,
        validators=[ValidateOnlyDigits()],
        verbose_name="Lotação - região",
        help_text="Somente números (2 dígitos)",
    )
    lotacao_batalhao = models.CharField(
        max_length=2,
        validators=[ValidateOnlyDigits()],
        verbose_name="Lotação - batalhão",
        help_text="Somente números (2 dígitos)",
    )
    lotacao_companhia = models.CharField(
        max_length=2,
        validators=[ValidateOnlyDigits()],
        verbose_name="Lotação - Companhia",
        help_text="Somente números (2 dígitos)",
    )
    lotacao_pelotao = models.CharField(
        max_length=2,
        validators=[ValidateOnlyDigits()],
        verbose_name="Lotação - pelotão",
        help_text="Somente números (2 dígitos)",
    )
    lotacao_grupo = models.CharField(
        max_length=1,
        validators=[ValidateOnlyDigits()],
        verbose_name="Lotação - grupo",
        help_text="Somente números (1 dígito)",
    )
    lotacao_cidade = models.CharField(
        max_length=50,
        verbose_name="Lotação - cidade",
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
        related_name="afastamentos",
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
        related_name="restricoes",
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
        verbose_name = "Policial: dados profissionais"
        verbose_name_plural = "Policiais: dados profissionais"
        ordering = ["policial__nome", "policial__sobrenome"]

    def __str__(self):
        return f"{self.policial.__str__()}"

    def clean(self):
        super().clean()
        self.lotacao_cidade = get_capitalized_words(self.lotacao_cidade)
        self.antiguidade = self.antiguidade.zfill(5)
        self.lotacao_regiao = self.lotacao_regiao.zfill(2)
        self.lotacao_batalhao = self.lotacao_batalhao.zfill(2)
        self.lotacao_companhia = self.lotacao_companhia.zfill(2)
        self.lotacao_pelotao = self.lotacao_pelotao.zfill(2)
        self.lotacao_grupo = self.lotacao_grupo.zfill(1)

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
        if self.proximas_ferias:
            return relativedelta(self.proximas_ferias, timezone.now().date())
        return None

    @property
    def tempo_afastamento(self):
        if self.afastamento_data_inicio and self.afastamento_data_fim:
            return relativedelta(self.afastamento_data_fim, self.afastamento_data_inicio)
        return None

    @property
    def tempo_restricao(self):
        if self.restricao_data_fim:
            return relativedelta(self.restricao_data_fim, timezone.now().date())
        return None

    @property
    def tempo_servico(self):
        return relativedelta(timezone.now().date(), self.data_ingresso)

    @property
    def tempo_trabalho_militar(self):
        tempo = relativedelta()
        trabalhos_anteriores = self.policial.trabalhos_anteriores.all()
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
        trabalhos_anteriores = self.policial.trabalhos_anteriores.all()
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
        t_masculino_dias = 30 * 365
        t_feminino_dias = 25 * 365
        t_masculino_anos = relativedelta(years=30)
        t_feminino_anos = relativedelta(years=25)
        t_masc_fem_anos = relativedelta(years=35)
        taxa = 0.17
        if data_ingresso <= data_limite:
            if policial_genero == Genero.MASCULINO:
                if not t_trabalho_nao_militar and not t_trabalho_militar:
                    pedagio += round(
                        (t_masculino_dias - (data_limite - data_ingresso).days) * taxa
                    )
                    aposentadoria = (
                        data_hoje + t_masculino_anos - t_servico + relativedelta(days=pedagio)
                    )
                elif t_trabalho_nao_militar and not t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= t_trabalho_nao_militar_max:
                        pedagio += round(
                            (
                                t_masculino_dias
                                - (data_limite - data_ingresso).days
                                - t_trabalho_nao_militar_max
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + t_masculino_anos
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            + relativedelta(days=pedagio)
                        )
                    else:
                        pedagio += round(
                            (
                                t_masculino_dias
                                - (data_limite - data_ingresso).days
                                - t_trabalho_nao_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + t_masculino_anos
                            - t_servico
                            - t_trabalho_nao_militar
                            + relativedelta(days=pedagio)
                        )
                elif t_trabalho_nao_militar and t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= t_trabalho_nao_militar_max:
                        pedagio += round(
                            (
                                t_masculino_dias
                                - (data_limite - data_ingresso).days
                                - t_trabalho_nao_militar_max
                                - t_trabalho_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + t_masculino_anos
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                    else:
                        pedagio += round(
                            (
                                t_masculino_dias
                                - (data_limite - data_ingresso).days
                                - t_trabalho_nao_militar.days
                                - t_trabalho_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + t_masculino_anos
                            - t_servico
                            - t_trabalho_nao_militar
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                elif not t_trabalho_nao_militar and t_trabalho_militar:
                    pedagio += round(
                        (
                            t_masculino_dias
                            - (data_limite - data_ingresso).days
                            - t_trabalho_militar.days
                        )
                        * taxa
                    )
                    aposentadoria = (
                        data_hoje
                        + t_masculino_anos
                        - t_servico
                        - t_trabalho_militar
                        + relativedelta(days=pedagio)
                    )
            elif policial_genero == Genero.FEMININO:
                if not t_trabalho_nao_militar and not t_trabalho_militar:
                    pedagio += round((t_feminino_dias - (data_limite - data_ingresso).days) * taxa)
                    aposentadoria = (
                        data_hoje + t_feminino_anos - t_servico + relativedelta(days=pedagio)
                    )
                elif t_trabalho_nao_militar and not t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= t_trabalho_nao_militar_max:
                        pedagio += round(
                            (
                                t_feminino_dias
                                - (data_limite - data_ingresso).days
                                - t_trabalho_nao_militar_max
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + t_feminino_anos
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            + relativedelta(days=pedagio)
                        )
                    else:
                        pedagio += round(
                            (
                                t_feminino_dias
                                - (data_limite - data_ingresso).days
                                - t_trabalho_nao_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + t_feminino_anos
                            - t_servico
                            - t_trabalho_nao_militar
                            + relativedelta(days=pedagio)
                        )
                elif t_trabalho_nao_militar and t_trabalho_militar:
                    if t_trabalho_nao_militar.days >= t_trabalho_nao_militar_max:
                        pedagio += round(
                            (
                                t_feminino_dias
                                - (data_limite - data_ingresso).days
                                - t_trabalho_nao_militar_max
                                - t_trabalho_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + t_feminino_anos
                            - t_servico
                            - relativedelta(days=t_trabalho_nao_militar_max)
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                    else:
                        pedagio += round(
                            (
                                t_feminino_dias
                                - (data_limite - data_ingresso).days
                                - t_trabalho_nao_militar.days
                                - t_trabalho_militar.days
                            )
                            * taxa
                        )
                        aposentadoria = (
                            data_hoje
                            + t_feminino_anos
                            - t_servico
                            - t_trabalho_nao_militar
                            - t_trabalho_militar
                            + relativedelta(days=pedagio)
                        )
                elif not t_trabalho_nao_militar and t_trabalho_militar:
                    pedagio += round(
                        (
                            t_feminino_dias
                            - (data_limite - data_ingresso).days
                            - t_trabalho_militar.days
                        )
                        * taxa
                    )
                    aposentadoria = (
                        data_hoje
                        + t_feminino_anos
                        - t_servico
                        - t_trabalho_militar
                        + relativedelta(days=pedagio)
                    )
        elif data_ingresso > data_limite:
            if not t_trabalho_nao_militar and not t_trabalho_militar:
                aposentadoria = (
                    data_hoje + t_masc_fem_anos - t_servico + relativedelta(days=pedagio)
                )
            elif t_trabalho_nao_militar and not t_trabalho_militar:
                if t_trabalho_nao_militar.days >= t_trabalho_nao_militar_max:
                    aposentadoria = (
                        data_hoje
                        + t_masc_fem_anos
                        - t_servico
                        - relativedelta(days=t_trabalho_nao_militar_max)
                        + relativedelta(days=pedagio)
                    )
                else:
                    aposentadoria = (
                        data_hoje
                        + t_masc_fem_anos
                        - t_servico
                        - t_trabalho_nao_militar
                        + relativedelta(days=pedagio)
                    )
            elif t_trabalho_nao_militar and t_trabalho_militar:
                if t_trabalho_nao_militar.days >= t_trabalho_nao_militar_max:
                    aposentadoria = (
                        data_hoje
                        + t_masc_fem_anos
                        - t_servico
                        - relativedelta(days=t_trabalho_nao_militar_max)
                        - t_trabalho_militar
                        + relativedelta(days=pedagio)
                    )
                else:
                    aposentadoria = (
                        data_hoje
                        + t_masc_fem_anos
                        - t_servico
                        - t_trabalho_nao_militar
                        - t_trabalho_militar
                        + relativedelta(days=pedagio)
                    )
            elif not t_trabalho_nao_militar and t_trabalho_militar:
                aposentadoria = (
                    data_hoje
                    + t_masc_fem_anos
                    - t_servico
                    - t_trabalho_militar
                    + relativedelta(days=pedagio)
                )
        return aposentadoria


class PolicialFormacaoComplementar(TimeStampedModel):
    id = UUIDField(primary_key=True, editable=False)
    policial = models.OneToOneField(
        Policial,
        on_delete=models.CASCADE,
        related_name="formacao_complementar",
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
        verbose_name = "Policial: formação complementar"
        verbose_name_plural = "Policiais: formações complementares"
        ordering = ["policial__nome", "policial__sobrenome"]

    def __str__(self):
        return f"{self.policial.__str__()}"


class PolicialTrabalhoAnterior(TimeStampedModel):
    id = UUIDField(primary_key=True, editable=False)
    policial = models.ForeignKey(
        Policial,
        on_delete=models.CASCADE,
        related_name="trabalhos_anteriores",
        verbose_name="Policial",
    )
    tipo = models.CharField(
        max_length=50,
        choices=TipoTrabalhoAnterior.choices,
        verbose_name="Tipo de trabalho anterior",
    )
    tempo = models.PositiveSmallIntegerField(
        verbose_name="Tempo de trabalho anterior (dias)",
    )

    class Meta:
        verbose_name = "Policial: trabalho anterior"
        verbose_name_plural = "Policiais: trabalhos anteriores"
        ordering = ["policial__nome", "policial__sobrenome"]
        unique_together = ("tipo", "policial")

    def __str__(self):
        return f"{self.policial.__str__()}: {self.get_tipo_display()} ({self.tempo} dias)"

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_tipo_display(self):
        return TipoTrabalhoAnterior(self.tipo).label
