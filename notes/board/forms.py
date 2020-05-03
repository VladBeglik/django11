from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import models


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = [
            'username',
            'email'
        ]
