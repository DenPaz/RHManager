from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import resolve
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import RegistroInicial


class PoliciaisListView(LoginRequiredMixin, ListView):
    model = RegistroInicial
    template_name = "cadastro/policiais/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"segment": resolve(self.request.path_info).view_name})
        return context
