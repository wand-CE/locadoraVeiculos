from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView
from django.contrib import messages
from veiculos.forms import CadUsuarioForm, CriarContratoForm, CriarClienteForm
from veiculos.models import Veiculo, TipoVeiculo, Contrato, Cliente
from django.contrib.auth.models import User


class HomeView(ListView):
    template_name = 'index.html'
    queryset = TipoVeiculo.tipoquery.all()
    context_object_name = 'cars'


class CadUsuarioView(FormView):
    template_name = 'usuario/cadastro.html'
    form_class = CadUsuarioForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, message='Usuario Cadastrado!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível cadastrar')
        return super().form_invalid(form)


class LoginUserView(FormView):
    template_name = 'usuario/login.html'
    model = User
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        senha = form.cleaned_data['password']
        usuario = authenticate(self.request, username=username, password=senha)
        if usuario is not None:
            login(self.request, usuario)
            return redirect('home')
        messages.error(self.request, 'Usuário não cadastrado')
        return redirect('loginusuario')

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível logar')
        return super().form_invalid(form)
        return redirect('loginusuario')


class LogoutUserView(LoginRequiredMixin, LogoutView):

    def get(self, request):
        logout(request)
        return redirect('home')


class CriarContratoView(LoginRequiredMixin, CreateView):
    template_name = 'servicos/criarContrato.html'
    model = Contrato
    form_class = CriarContratoForm
    success_url = reverse_lazy('criarContrato')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data()
        contexto['form_criar_cliente'] = CriarClienteForm
        return contexto

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, message='Contrato não cadastrado')
        return reverse_lazy('criarContrato')


class CriarClienteView(LoginRequiredMixin, FormView):
    template_name = 'servicos/criarCliente.html'
    form_class = CriarClienteForm

    def form_valid(self, form, *args, **kwargs):
        dados = form.cleaned_data
        novo_cliente = Cliente.objects.create(
            nome=dados['nome'],
            numHab=dados['numHab'],
            endereco=dados['endereco'],
            telefone=dados['telefone'])
        novo_cliente.save()
        return JsonResponse({'cliente': f'{novo_cliente}'})
