from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
    )
    fieldsets = (
        (
            "Credenciais de acesso",
            {"fields": ("username", "password")},
        ),
        (
            "Informações pessoais",
            {"fields": ("first_name", "last_name", "profile_picture")},
        ),
        (
            "Permissões de acesso",
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        (
            "Permissões de usuário",
            {"fields": ("user_permissions",)},
        ),
        (
            "Datas importantes",
            {"fields": ("last_login", "date_joined")},
        ),
    )
    add_fieldsets = (
        (
            "Credenciais de acesso",
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
        (
            "Informações pessoais",
            {"fields": ("first_name", "last_name", "profile_picture")},
        ),
    )
    ordering = ("username",)
    filter_horizontal = ("user_permissions",)
    list_per_page = 10
    readonly_fields = (
        "last_login",
        "date_joined",
    )


admin.site.unregister(Group)
