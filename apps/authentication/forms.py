from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Usuário",
                "class": "form-control",
                "id": "id_username",
            }
        ),
        required=True,
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Senha",
                "class": "form-control",
                "id": "id_password",
            },
        ),
        required=True,
    )
