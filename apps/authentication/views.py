from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from .forms import LoginForm


class LoginView(View):
    form_class = LoginForm
    template_name = "authentication/login.html"
    redirect_authenticated_user = True
    success_url = settings.LOGIN_REDIRECT_URL

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            User = get_user_model()
            user = User.objects.filter(username=username).first()
            if user is not None:
                if user.is_active:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect(self.success_url)
                    else:
                        messages.error(request, "Senha inválida.")
                else:
                    messages.error(request, "Usuário inativo.")
            else:
                messages.error(request, "Usuário não encontrado.")
        else:
            messages.error(request, "Erro ao validar o formulário.")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    success_url = settings.LOGOUT_REDIRECT_URL

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Logout realizado com sucesso.")
        return redirect(self.success_url)

    get = post
