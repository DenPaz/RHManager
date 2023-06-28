from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import resolve
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Policial, PolicialDadosPessoais


class PoliciaisListView(LoginRequiredMixin, ListView):
    model = Policial
    template_name = "cadastro/policiais/list.html"
    context_object_name = "policiais"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["segment"] = resolve(self.request.path_info).view_name
        return context
