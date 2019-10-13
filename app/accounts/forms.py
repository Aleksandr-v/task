from django import forms
from .models import Message


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label='Пароль'
    )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('sender', 'body')
        labels = {
            "sender": "Электронная почта",
            "body": "Сообщение"
        }
