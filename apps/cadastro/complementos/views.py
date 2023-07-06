from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.urls import resolve, reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
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
from .resources import (
    CursoCivilResource,
    CursoPMResource,
    CursoResource,
    FormacaoAcademicaResource,
    LinguaEstrangeiraResource,
    TipoAfastamentoResource,
    TipoRestricaoResource,
)


class DadoComplementarListView(LoginRequiredMixin, ListView):
    template_name = "cadastro/complementos/list.html"
    ordering = ["label"]
    paginate_by = 9
    page_title = ""
    page_description = ""
    page_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = resolve(self.request.path_info).view_name
        context["page_title"] = self.page_title
        context["page_description"] = self.page_description
        context["export_url"] = reverse(f"cadastro:complementos:{self.page_name}_list")
        context["list_url"] = reverse(f"cadastro:complementos:{self.page_name}_list")
        context["create_url"] = reverse(f"cadastro:complementos:{self.page_name}_create")
        # context["update_url"] = reverse(f"cadastro:complementos:{self.page_name}_update")
        # context["delete_url"] = reverse(f"cadastro:complementos:{self.page_name}_delete")
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(Q(label__icontains=search_query))
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
            response["Content-Disposition"] = f'attachment; filename="{self.page_name}.csv"'
            response.write(dataset.csv)
        elif format_type == "xls":
            response = HttpResponse(content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = f'attachment; filename="{self.page_name}.xls"'
            response.write(dataset.xls)
        elif format_type == "xlsx":
            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = f'attachment; filename="{self.page_name}.xlsx"'
            response.write(dataset.xlsx)
        else:
            return JsonResponse({"error": "Formato não suportado."}, status=400)
        return response


class DadoComplementarCreateView(LoginRequiredMixin, CreateView):
    template_name = "cadastro/complementos/create.html"
    fields = ["label"]
    page_title = ""
    page_description = ""
    page_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = resolve(self.request.path_info).view_name
        context["page_title"] = self.page_title
        context["page_description"] = self.page_description
        context["page_name"] = self.page_name
        context["list_url"] = reverse(f"cadastro:complementos:{self.page_name}_list")
        return context


class FormacaoAcademicaMixin:
    model = FormacaoAcademica
    page_title = "Formações acadêmicas"
    resource_class = FormacaoAcademicaResource
    page_name = "formacao_academica"
    success_url = reverse_lazy("cadastro:complementos:formacao_academica_list")


class CursoMixin:
    model = Curso
    page_title = "Cursos"
    resource_class = CursoResource
    page_name = "curso_geral"
    success_url = reverse_lazy("cadastro:complementos:curso_geral_list")


class CursoPMMixin:
    model = CursoPM
    page_title = "Cursos da PM"
    resource_class = CursoPMResource
    page_name = "curso_pm"
    success_url = reverse_lazy("cadastro:complementos:curso_pm_list")


class CursoCivilMixin:
    model = CursoCivil
    page_title = "Cursos Civis"
    resource_class = CursoCivilResource
    page_name = "curso_civil"
    success_url = reverse_lazy("cadastro:complementos:curso_civil_list")


class LinguaEstrangeiraMixin:
    model = LinguaEstrangeira
    page_title = "Línguas estrangeiras"
    resource_class = LinguaEstrangeiraResource
    page_name = "lingua_estrangeira"
    success_url = reverse_lazy("cadastro:complementos:lingua_estrangeira_list")


class TipoAfastamentoMixin:
    model = TipoAfastamento
    page_title = "Tipos de afastamento"
    resource_class = TipoAfastamentoResource
    page_name = "tipo_afastamento"
    success_url = reverse_lazy("cadastro:complementos:tipo_afastamento_list")


class TipoRestricaoMixin:
    model = TipoRestricao
    page_title = "Tipos de restrição"
    resource_class = TipoRestricaoResource
    page_name = "tipo_restricao"
    success_url = reverse_lazy("cadastro:complementos:tipo_restricao_list")


class FormacaoAcademicaListView(FormacaoAcademicaMixin, DadoComplementarListView):
    page_description = "Formações acadêmicas cadastradas"


class CursoListView(CursoMixin, DadoComplementarListView):
    page_description = "Cursos gerais cadastrados"


class CursoPMListView(CursoPMMixin, DadoComplementarListView):
    page_description = "Cursos da PM cadastrados"


class CursoCivilListView(CursoCivilMixin, DadoComplementarListView):
    page_description = "Cursos Civis cadastrados"


class LinguaEstrangeiraListView(LinguaEstrangeiraMixin, DadoComplementarListView):
    page_description = "Línguas estrangeiras cadastradas"


class TipoAfastamentoListView(TipoAfastamentoMixin, DadoComplementarListView):
    page_description = "Tipos de afastamentos cadastrados"


class TipoRestricaoListView(TipoRestricaoMixin, DadoComplementarListView):
    page_description = "Tipos de restrições cadastrados"


class FormacaoAcademicaCreateView(FormacaoAcademicaMixin, DadoComplementarCreateView):
    page_description = "Cadastrar nova formação acadêmica"


class CursoCreateView(CursoMixin, DadoComplementarCreateView):
    page_description = "Cadastrar novo curso geral"


class CursoPMCreateView(CursoPMMixin, DadoComplementarCreateView):
    page_description = "Cadastrar novo curso da PM"


class CursoCivilCreateView(CursoCivilMixin, DadoComplementarCreateView):
    page_description = "Cadastrar novo curso civil"


class LinguaEstrangeiraCreateView(LinguaEstrangeiraMixin, DadoComplementarCreateView):
    page_description = "Cadastrar nova língua estrangeira"


class TipoAfastamentoCreateView(TipoAfastamentoMixin, DadoComplementarCreateView):
    page_description = "Cadastrar novo tipo de afastamento"


class TipoRestricaoCreateView(TipoRestricaoMixin, DadoComplementarCreateView):
    page_description = "Cadastrar novo tipo de restrição"
