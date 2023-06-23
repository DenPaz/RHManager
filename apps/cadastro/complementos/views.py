from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class DadoComplementarView(LoginRequiredMixin, View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = "cadastro:dados"
        return context


class CursoView(DadoComplementarView):
    pass
