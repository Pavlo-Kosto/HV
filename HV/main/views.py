from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
# Подключение новой формы для регистрации
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterUserForm, LoginUserForm
import datetime


def get_timestamp():
    return datetime.datetime.now().__hash__()


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    template_name = 'main/login.html'
    form_class = LoginUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


def Logout_User(request):
    logout(request)
    return redirect('login')


def index(request):
    data = {
        'title': 'Главная страница',
        'values': ['some', 'home', '123'],
        'get_timestamp': get_timestamp
    }
    return render(request, 'main/index.html', data)


def about(request):
    return render(request, 'main/about.html')
