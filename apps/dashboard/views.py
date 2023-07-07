from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import resolve
from django.views.generic import TemplateView

from apps.cadastro.policiais.models import Policial, PolicialFormacaoComplementar


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"segment": resolve(self.request.path_info).view_name})
        context["policiais"] = Policial.objects.all()
        context["policiais_masculinos"] = Policial.objects.filter(genero="M").count()
        context["policiais_femininos"] = Policial.objects.filter(genero="F").count()
        context["policiais_linguas_estrangeiras"] = PolicialFormacaoComplementar.objects.filter(
            linguas_estrangeiras__isnull=False
        ).count()
        return context
