from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.urls import resolve, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    PolicialDadosPessoaisForm,
    PolicialDadosProfissionaisForm,
    PolicialForm,
    PolicialFormacaoComplementarForm,
    PolicialTrabalhoAnteriorForm,
)
from .models import Policial, PolicialTrabalhoAnterior
from .resources import PolicialMixedExportResource


class PoliciaisListView(LoginRequiredMixin, ListView):
    model = Policial
    template_name = "cadastro/policiais/list.html"
    ordering = ["nome", "sobrenome"]
    resource_class = PolicialMixedExportResource
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = resolve(self.request.path_info).view_name
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(matricula__icontains=search_query)
                | Q(nome__icontains=search_query)
                | Q(sobrenome__icontains=search_query)
                | Q(cpf__icontains=search_query)
            )
        return queryset.order_by(*self.ordering)

    def get(self, request, *args, **kwargs):
        if request.GET.get("format"):
            return self.export_data(request)
        return super().get(request, *args, **kwargs)

    def export_data(self, request):
        format_type = request.GET.get("format")
        dataset = self.resource_class().export()
        if format_type == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="policiais.csv"'
            response.write(dataset.csv)
        elif format_type == "xls":
            response = HttpResponse(content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = 'attachment; filename="policiais.xls"'
            response.write(dataset.xls)
        elif format_type == "xlsx":
            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = 'attachment; filename="policiais.xlsx"'
            response.write(dataset.xlsx)
        else:
            return JsonResponse({"error": "Formato não suportado."}, status=400)
        return response


class PoliciaisCreateView(LoginRequiredMixin, CreateView):
    model = Policial
    form_class = PolicialForm
    template_name = "cadastro/policiais/create.html"
    success_url = reverse_lazy("cadastro:policiais:list")
    success_message = "Policial cadastrado com sucesso!"

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

            messages.success(self.request, self.success_message)
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))


class PoliciaisUpdateView(LoginRequiredMixin, UpdateView):
    model = Policial
    form_class = PolicialForm
    template_name = "cadastro/policiais/update.html"
    success_url = reverse_lazy("cadastro:policiais:list")
    success_message = "Policial atualizado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super(PoliciaisUpdateView, self).get_context_data(**kwargs)
        context["segment"] = resolve(self.request.path_info).view_name

        PolicialTrabalhoAnteriorFormSet = inlineformset_factory(
            Policial,
            PolicialTrabalhoAnterior,
            form=PolicialTrabalhoAnteriorForm,
            extra=1,
            can_delete=True,
        )

        if self.request.POST:
            context["policiais_form"] = PolicialForm(self.request.POST, instance=self.object)
            try:
                context["policiais_dados_pessoais_form"] = PolicialDadosPessoaisForm(
                    self.request.POST, instance=self.object.dados_pessoais
                )
            except Policial.dados_pessoais.RelatedObjectDoesNotExist:
                context["policiais_dados_pessoais_form"] = PolicialDadosPessoaisForm(
                    self.request.POST
                )
            try:
                context["policiais_dados_profissionais_form"] = PolicialDadosProfissionaisForm(
                    self.request.POST, instance=self.object.dados_profissionais
                )
            except Policial.dados_profissionais.RelatedObjectDoesNotExist:
                context["policiais_dados_profissionais_form"] = PolicialDadosProfissionaisForm(
                    self.request.POST
                )
            try:
                context["policiais_formacao_complementar_form"] = PolicialFormacaoComplementarForm(
                    self.request.POST, instance=self.object.formacao_complementar
                )
            except Policial.formacao_complementar.RelatedObjectDoesNotExist:
                context["policiais_formacao_complementar_form"] = PolicialFormacaoComplementarForm(
                    self.request.POST
                )
            context["policiais_trabalho_anterior_formset"] = PolicialTrabalhoAnteriorFormSet(
                self.request.POST, instance=self.object, prefix="trabalhos_anteriores"
            )
        else:
            context["policiais_form"] = PolicialForm(instance=self.object)
            try:
                context["policiais_dados_pessoais_form"] = PolicialDadosPessoaisForm(
                    instance=self.object.dados_pessoais
                )
            except Policial.dados_pessoais.RelatedObjectDoesNotExist:
                context["policiais_dados_pessoais_form"] = PolicialDadosPessoaisForm()
            try:
                context["policiais_dados_profissionais_form"] = PolicialDadosProfissionaisForm(
                    instance=self.object.dados_profissionais
                )
            except Policial.dados_profissionais.RelatedObjectDoesNotExist:
                context["policiais_dados_profissionais_form"] = PolicialDadosProfissionaisForm()
            try:
                context["policiais_formacao_complementar_form"] = PolicialFormacaoComplementarForm(
                    instance=self.object.formacao_complementar
                )
            except Policial.formacao_complementar.RelatedObjectDoesNotExist:
                context[
                    "policiais_formacao_complementar_form"
                ] = PolicialFormacaoComplementarForm()

            context["policiais_trabalho_anterior_formset"] = PolicialTrabalhoAnteriorFormSet(
                instance=self.object, prefix="trabalhos_anteriores"
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        policiais_form = context["policiais_form"]
        policiais_dados_pessoais_form = context["policiais_dados_pessoais_form"]
        policiais_dados_profissionais_form = context["policiais_dados_profissionais_form"]
        policiais_formacao_complementar_form = context["policiais_formacao_complementar_form"]
        policiais_trabalho_anterior_formset = context["policiais_trabalho_anterior_formset"]

        if (
            policiais_form.is_valid()
            and policiais_dados_pessoais_form.is_valid()
            and policiais_dados_profissionais_form.is_valid()
            and policiais_formacao_complementar_form.is_valid()
            and policiais_trabalho_anterior_formset.is_valid()
        ):
            self.object = form.save()
            policiais_dados_pessoais = policiais_dados_pessoais_form.save(commit=False)
            policiais_dados_profissionais = policiais_dados_profissionais_form.save(commit=False)
            policiais_formacao_complementar = policiais_formacao_complementar_form.save(
                commit=False
            )

            policiais_dados_pessoais.policial = self.object
            policiais_dados_profissionais.policial = self.object
            policiais_formacao_complementar.policial = self.object

            policiais_dados_pessoais.save()
            policiais_dados_profissionais.save()
            policiais_formacao_complementar.save()

            policiais_trabalho_anterior_formset.save()

            messages.success(self.request, self.success_message)
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))


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
