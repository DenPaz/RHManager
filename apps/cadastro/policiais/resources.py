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


class PolicialMixedExportResource(PolicialBaseResource):
    formacao_academica = fields.Field(
        column_name="formacao_academica",
        attribute="dados_profissionais__formacao_academica",
        widget=ManyToManyWidget(FormacaoAcademica, field="label"),
    )
    afastamento = fields.Field(
        column_name="afastamento",
        attribute="dados_profissionais__afastamento",
        widget=ForeignKeyWidget(TipoAfastamento, field="label"),
    )
    restricao = fields.Field(
        column_name="restricao",
        attribute="dados_profissionais__restricao",
        widget=ForeignKeyWidget(TipoRestricao, field="label"),
    )
    cursos = fields.Field(
        column_name="cursos",
        attribute="formacao_complementar__cursos",
        widget=ManyToManyWidget(Curso, field="label"),
    )
    cursos_pm = fields.Field(
        column_name="cursos_pm",
        attribute="formacao_complementar__cursos_pm",
        widget=ManyToManyWidget(CursoPM, field="label"),
    )
    cursos_civis = fields.Field(
        column_name="cursos_civis",
        attribute="formacao_complementar__cursos_civis",
        widget=ManyToManyWidget(CursoCivil, field="label"),
    )
    linguas_estrangeiras = fields.Field(
        column_name="linguas_estrangeiras",
        attribute="formacao_complementar__linguas_estrangeiras",
        widget=ManyToManyWidget(LinguaEstrangeira, field="label"),
    )

    def init_instance(self, *args, **kwargs):
        super().init_instance(*args, **kwargs)
        self.formacao_academica.widget = ManyToManyWidget(
            FormacaoAcademica.objects.all(), field="label"
        )
        self.afastamento.widget = ForeignKeyWidget(TipoAfastamento.objects.all(), field="label")
        self.restricao.widget = ForeignKeyWidget(TipoRestricao.objects.all(), field="label")
        self.cursos.widget = ManyToManyWidget(Curso.objects.all(), field="label")
        self.cursos_pm.widget = ManyToManyWidget(CursoPM.objects.all(), field="label")
        self.cursos_civis.widget = ManyToManyWidget(CursoCivil.objects.all(), field="label")
        self.linguas_estrangeiras.widget = ManyToManyWidget(
            LinguaEstrangeira.objects.all(), field="label"
        )

    class Meta:
        model = Policial
        fields = (
            "matricula",
            "nome",
            "sobrenome",
            "cpf",
            "genero",
            "nome_guerra",
            "dados_pessoais__nome_guerra",
            "dados_pessoais__data_nascimento",
            "dados_pessoais__tipo_sanguineo",
            "dados_pessoais__celular",
            "dados_pessoais__email",
            "dados_pessoais__endereco_logradouro",
            "dados_pessoais__endereco_numero",
            "dados_pessoais__endereco_bairro",
            "dados_pessoais__endereco_cidade",
            "dados_pessoais__endereco_estado",
            "dados_pessoais__endereco_cep",
            "dados_profissionais__data_ingresso",
            "dados_profissionais__antiguidade",
            "dados_profissionais__lotacao_regiao",
            "dados_profissionais__lotacao_batalhao",
            "dados_profissionais__lotacao_companhia",
            "dados_profissionais__lotacao_pelotao",
            "dados_profissionais__lotacao_grupo",
            "dados_profissionais__lotacao_cidade",
            "dados_profissionais__comportamento",
            "dados_profissionais__proximas_ferias",
            "dados_profissionais__licencas_especiais_acumuladas",
            "dados_profissionais__afastamento_data_inicio",
            "dados_profissionais__afastamento_data_fim",
            "dados_profissionais__restricao_data_fim",
            "dados_profissionais__observacoes",
        )


# this class is used to import data from all the models
# class PolicialMixedImportResource(resources.ModelResource):
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
