import csv
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import resolve, reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    CVSUploadForm,
    PolicialDadosPessoaisForm,
    PolicialDadosProfissionaisForm,
    PolicialForm,
    PolicialFormacaoComplementarForm,
    PolicialTrabalhoAnteriorForm,
)
from .models import (
    Policial,
    PolicialDadosPessoais,
    PolicialDadosProfissionais,
    PolicialFormacaoComplementar,
    PolicialTrabalhoAnterior,
)
from .resources import PolicialResource


class PoliciaisListView(LoginRequiredMixin, ListView):
    model = Policial
    template_name = "cadastro/policiais/list.html"
    context_object_name = "policiais"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = resolve(self.request.path_info).view_name
        return context

    def get_queryset(self):
        search_query = self.request.GET.get("search", "")
        if search_query:
            return Policial.objects.filter(nome__icontains=search_query)
        return Policial.objects.all()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if "export_csv" in request.GET:
            return self.export_csv(request)
        return response

    def post(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if "import_csv" in request.POST:
            return self.import_csv(request)
        return response

    def export_csv(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="policiais.csv"'
        writer = csv.writer(response)
        resource = PolicialResource()
        fields = resource.get_fields()
        writer.writerow([field.column_name for field in fields])
        for policial in self.get_queryset():
            writer.writerow(field.export(policial) for field in fields)
        return response

    def import_csv(self, request):
        form = CVSUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resource = PolicialResource()
            dataset = resource.import_data(request.FILES["file"])
            result = resource.import_data(dataset, dry_run=True)
            if not result.has_errors():
                resource.import_data(dataset, dry_run=False)
                return redirect("cadastro:policiais:list")
        return self.get(request)


class PoliciaisCreateView(LoginRequiredMixin, CreateView):
    model = Policial
    form_class = PolicialForm
    template_name = "cadastro/policiais/create.html"
    success_url = reverse_lazy("cadastro:policiais:list")

    def get_context_data(self, **kwargs):
        context = super(PoliciaisCreateView, self).get_context_data(**kwargs)
        context["segment"] = resolve(self.request.path_info).view_name
        if self.request.POST:
            context["policiais_form"] = PolicialForm(self.request.POST)
            context["policiais_dados_pessoais_form"] = PolicialDadosPessoaisForm(self.request.POST)
            context["policiais_dados_profissionais_form"] = PolicialDadosProfissionaisForm(
                self.request.POST
            )
            context["policiais_formacao_complementar_form"] = PolicialFormacaoComplementarForm(
                self.request.POST
            )
            context["policiais_trabalho_anterior_form"] = PolicialTrabalhoAnteriorForm(
                self.request.POST
            )
        else:
            context["policiais_form"] = PolicialForm()
            context["policiais_dados_pessoais_form"] = PolicialDadosPessoaisForm()
            context["policiais_dados_profissionais_form"] = PolicialDadosProfissionaisForm()
            context["policiais_formacao_complementar_form"] = PolicialFormacaoComplementarForm()
            context["policiais_trabalho_anterior_form"] = PolicialTrabalhoAnteriorForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        policiais_form = context["policiais_form"]
        policiais_dados_pessoais_form = context["policiais_dados_pessoais_form"]
        policiais_dados_profissionais_form = context["policiais_dados_profissionais_form"]
        policiais_formacao_complementar_form = context["policiais_formacao_complementar_form"]
        policiais_trabalho_anterior_form = context["policiais_trabalho_anterior_form"]

        if (
            policiais_form.is_valid()
            and policiais_dados_pessoais_form.is_valid()
            and policiais_dados_profissionais_form.is_valid()
            and policiais_formacao_complementar_form.is_valid()
            and policiais_trabalho_anterior_form.is_valid()
        ):
            self.object = form.save()
            policiais_dados_pessoais = policiais_dados_pessoais_form.save(commit=False)
            policiais_dados_profissionais = policiais_dados_profissionais_form.save(commit=False)
            policiais_formacao_complementar = policiais_formacao_complementar_form.save(
                commit=False
            )
            policiais_trabalho_anterior = policiais_trabalho_anterior_form.save(commit=False)

            policiais_dados_pessoais.policial = self.object
            policiais_dados_profissionais.policial = self.object
            policiais_formacao_complementar.policial = self.object
            policiais_trabalho_anterior.policial = self.object

            policiais_dados_pessoais.save()
            policiais_dados_profissionais.save()
            policiais_formacao_complementar.save()
            policiais_trabalho_anterior.save()

            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))


class PoliciaisUpdateView(LoginRequiredMixin, UpdateView):
    model = Policial
    form_class = PolicialForm
    template_name = "cadastro/policiais/update.html"
    success_url = reverse_lazy("cadastro:policiais:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = resolve(self.request.path_info).view_name
        return context


class PolicialDeleteView(LoginRequiredMixin, DeleteView):
    model = Policial
    success_url = reverse_lazy("cadastro:policiais:list")
    template_name = "cadastro/policiais/delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = resolve(self.request.path_info).view_name
        return context


class PolicialDetailView(LoginRequiredMixin, DetailView):
    model = Policial
    template_name = "cadastro/policiais/detail.html"
    form_class = PolicialForm
    success_url = reverse_lazy("cadastro:policiais:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = resolve(self.request.path_info).view_name
        return context
