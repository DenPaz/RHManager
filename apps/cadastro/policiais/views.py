import csv
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import resolve, reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PolicialForm
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


class PoliciaisCreateView(LoginRequiredMixin, CreateView):
    model = Policial
    template_name = "cadastro/policiais/create.html"
    form_class = PolicialForm
    success_url = reverse_lazy("cadastro:policiais:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = resolve(self.request.path_info).view_name
        return context


class PoliciaisUpdateView(LoginRequiredMixin, UpdateView):
    model = Policial
    template_name = "cadastro/policiais/update.html"
    form_class = PolicialForm
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
