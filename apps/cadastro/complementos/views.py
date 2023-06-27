from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .models import (
    Curso,
    CursoCivil,
    CursoPM,
    FormacaoAcademica,
    LinguaEstrangeira,
    TipoAfastamento,
    TipoRestricao,
)


class ComplementosListView(LoginRequiredMixin, View):
    template_name = "cadastro/complementos/list.html"

    def get(self, request):
        context = {
            "cursos": Curso.objects.all(),
            "cursos_civil": CursoCivil.objects.all(),
            "cursos_pm": CursoPM.objects.all(),
            "formacoes_academicas": FormacaoAcademica.objects.all(),
            "linguas_estrangeiras": LinguaEstrangeira.objects.all(),
            "tipos_afastamento": TipoAfastamento.objects.all(),
            "tipos_restricao": TipoRestricao.objects.all(),
            "segment": resolve(self.request.path_info).view_name,
        }
        return render(request, self.template_name, context)
