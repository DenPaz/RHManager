from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


class PolicialListView(LoginRequiredMixin, ListView):
    pass
