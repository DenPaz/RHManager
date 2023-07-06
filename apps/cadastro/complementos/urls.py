from django.urls import path

from .views import (
    CursoCivilCreateView,
    CursoCivilListView,
    CursoCreateView,
    CursoListView,
    CursoPMCreateView,
    CursoPMListView,
    FormacaoAcademicaCreateView,
    FormacaoAcademicaListView,
    LinguaEstrangeiraCreateView,
    LinguaEstrangeiraListView,
    TipoAfastamentoCreateView,
    TipoAfastamentoListView,
    TipoRestricaoCreateView,
    TipoRestricaoListView,
)

app_name = "complementos"

urlpatterns = [
    path(
        route="formacao-academica/list/",
        view=FormacaoAcademicaListView.as_view(),
        name="formacao_academica_list",
    ),
    path(
        route="curso/list/",
        view=CursoListView.as_view(),
        name="curso_geral_list",
    ),
    path(
        route="curso-pm/list/",
        view=CursoPMListView.as_view(),
        name="curso_pm_list",
    ),
    path(
        route="curso-civil/list/",
        view=CursoCivilListView.as_view(),
        name="curso_civil_list",
    ),
    path(
        route="lingua-estrangeira/list/",
        view=LinguaEstrangeiraListView.as_view(),
        name="lingua_estrangeira_list",
    ),
    path(
        route="tipo-afastamento/list/",
        view=TipoAfastamentoListView.as_view(),
        name="tipo_afastamento_list",
    ),
    path(
        route="tipo-restricao/list/",
        view=TipoRestricaoListView.as_view(),
        name="tipo_restricao_list",
    ),
    path(
        route="formacao-academica/create/",
        view=FormacaoAcademicaCreateView.as_view(),
        name="formacao_academica_create",
    ),
    path(
        route="curso/create/",
        view=CursoCreateView.as_view(),
        name="curso_geral_create",
    ),
    path(
        route="curso-pm/create/",
        view=CursoPMCreateView.as_view(),
        name="curso_pm_create",
    ),
    path(
        route="curso-civil/create/",
        view=CursoCivilCreateView.as_view(),
        name="curso_civil_create",
    ),
    path(
        route="lingua-estrangeira/create/",
        view=LinguaEstrangeiraCreateView.as_view(),
        name="lingua_estrangeira_create",
    ),
    path(
        route="tipo-afastamento/create/",
        view=TipoAfastamentoCreateView.as_view(),
        name="tipo_afastamento_create",
    ),
    path(
        route="tipo-restricao/create/",
        view=TipoRestricaoCreateView.as_view(),
        name="tipo_restricao_create",
    ),
]
