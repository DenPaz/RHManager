from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.templatetags.static import static

from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        verbose_name="Usuário",
        help_text="Obrigatório. 30 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.",
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Nome",
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Sobrenome",
    )
    email = None
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Superusuário",
        help_text="Designa se o usuário tem todas as permissões (incluindo acesso ao painel administrativo).",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Membro da equipe",
        help_text="Designa se o usuário pode acessar o painel administrativo.",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Designa se o usuário pode fazer login no sistema. Desmarque essa opção em vez de excluir contas.",
    )
    profile_picture = models.ImageField(
        upload_to="images/profile_pictures",
        blank=True,
        verbose_name="Foto de perfil",
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["username"]

    def __str__(self):
        return self.get_full_name()

    def clean(self):
        super().clean()
        if self.is_superuser and not self.is_staff:
            raise ValidationError("Superusuários devem ser também membros da equipe.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.get_short_name()

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.username

    def get_profile_picture(self):
        if self.profile_picture and hasattr(self.profile_picture, "url"):
            return self.profile_picture.url
        return static("images/user.png")
