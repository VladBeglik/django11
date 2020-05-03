from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import models


class LoginForm(auth_forms.AuthenticationForm):
    username = auth_forms.UsernameField(
        label='username',
        widget=forms.TextInput(
            attrs={'autofocus': True}
        )
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password'}
        ),
    )


class CreateUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = models.User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        return user
