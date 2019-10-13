from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .forms import LoginForm, MessageForm
from .utils import send_feedback
from .models import Message

import requests
import json
from smtplib import SMTPAuthenticationError


User = get_user_model()


class FeedbackView(LoginRequiredMixin, FormView):
    login_url = '/'
    template_name = 'accounts/feedback.html'
    form_class = MessageForm

    def form_valid(self, form):
        errors = []
        cd = form.cleaned_data
        message = Message(sender=cd['sender'], body=cd['body'])

        r = requests.get('http://jsonplaceholder.typicode.com/users')
        senders = json.loads(r.text)
        sender = {}
        for s in senders:
            if s['email'].lower() == cd['sender'].lower():
                sender = s
        try:
            send_feedback(cd['body'], cd['sender'], sender)
            message.status = 'Ok'
            message.save()
            return JsonResponse({
                'success': True,
                'message': 'Письмо успешно отправлено'
            })
        except (SMTPAuthenticationError,) as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            err = template.format(type(ex).__name__, ex.args)
            print(err)

            message.status = 'Error'
            message.save()
            errors.append(
                'Не удалось отправить сообщение. Повторите попытку позже'
            )
            return JsonResponse({
                'success': False,
                'errors': errors
            })

    def form_invalid(self, form):
        errors = []
        for k, v in form.errors.items():
            for e in v:
                errors.append(e)
        return JsonResponse({
            'success': False,
            'errors': errors
        })


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        errors = []
        cd = form.cleaned_data
        username = cd['username']
        password = cd['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return JsonResponse({'success': True})

        else:
            errors.append('Введите правильное имя пользователя и пароль')
            return JsonResponse({
                'success': False,
                'errors': errors
            })

    def form_invalid(self, form):
        errors = []
        for k, v in form.errors.items():
            for e in v:
                errors.append(e)
        return JsonResponse({
            'success': False,
            'errors': errors
        })


class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        cd = form.cleaned_data
        user = User(username=cd['username'])
        user.set_password(cd['password1'])
        user.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        errors = []
        for k, v in form.errors.items():
            for e in v:
                errors.append(e)
        return JsonResponse({
            'success': False,
            'errors': errors
        })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')
