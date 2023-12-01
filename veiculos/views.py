from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from veiculos.forms import CadUsuarioForm, CriarContratoForm, CriarClienteForm, OnibusForm, AutomovelForm
from veiculos.models import Veiculo, TipoVeiculo, Contrato, Cliente, Automovel, Onibus
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


class CriarVeiculoView(LoginRequiredMixin, TemplateView):
    template_name = 'servicos/veiculos/criarVeiculo.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data()
        contexto['form_automovel'] = AutomovelForm
        contexto['form_onibus'] = OnibusForm
        contexto['radio_checked'] = 'automovel'
        return contexto

    def post(self, request):
        tipo_veiculo = request.POST.get('tipo_veiculo', None)

        form = None
        if tipo_veiculo:
            if tipo_veiculo == 'onibus':
                form = OnibusForm(request.POST, request.FILES)
            elif tipo_veiculo == 'automovel':
                form = AutomovelForm(request.POST, request.FILES)

        if form and form.is_valid():
            form.save()
            return redirect('listaVeiculos')
        elif form and not form.is_valid():
            if isinstance(form, AutomovelForm):
                return render(request, self.template_name, {
                    'form_automovel': form,
                    'form_onibus': OnibusForm(),
                    'radio_checked': 'automovel',
                })
            elif isinstance(form, OnibusForm):
                return render(request, self.template_name, {
                    'form_automovel': AutomovelForm,
                    'form_onibus': form,
                    'radio_checked': 'onibus',
                })

        return redirect('listaVeiculos')


class ListarVeiculoView(LoginRequiredMixin, ListView):
    template_name = 'servicos/veiculos/listaVeiculos.html'
    model = Veiculo
    context_object_name = 'veiculos'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data()
        contexto['veiculos'] = {'automoveis': [], 'onibus': []}

        for automovel in Automovel.tipoquery.all():
            placa = Veiculo.objects.get(tipoVeiculo=automovel).placa

            elemento = {}

            elemento['foto'] = automovel.foto
            elemento['nome'] = automovel.nome
            elemento['tipo'] = 'Automóvel'
            elemento['placa'] = placa
            elemento['id'] = automovel.id

            contexto['veiculos']['automoveis'].append(elemento)

        for onibus in Onibus.tipoquery.all():
            placa = Veiculo.objects.get(tipoVeiculo=onibus).placa

            elemento = {}
            elemento['foto'] = onibus.foto
            elemento['nome'] = onibus.nome
            elemento['tipo'] = 'Ônibus'
            elemento['placa'] = placa
            elemento['id'] = onibus.id

            contexto['veiculos']['onibus'].append(elemento)

        return contexto


class RemoverVeiculoView(DeleteView):
    model = TipoVeiculo
    template_name = 'servicos/veiculos/removerVeiculo.html'
    success_url = reverse_lazy('listaVeiculos')


class EditarVeiculoView(UpdateView):
    template_name = 'servicos/veiculos/editarCliente.html'
    success_url = reverse_lazy('listaVeiculos')
    model = TipoVeiculo

    def get_form_class(self):
        form_type = self.kwargs.get('tipoVeiculo', None)

        if form_type == 'Automóvel':
            return AutomovelForm
        elif form_type == 'Ônibus':
            return OnibusForm

        raise Http404

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data()
        contexto['nome_tipo_veiculo'] = 'Automóvel' if 'w' else 'Ônibus'
        print(contexto['nome_tipo_veiculo'])
        print(type(self.form_class))

        return contexto


class CriarClienteView(LoginRequiredMixin, FormView):
    template_name = 'servicos/clientes/criarCliente.html'
    form_class = CriarClienteForm

    def post(self, request, *args, **kwargs):
        form = CriarClienteForm(request.POST)
        input_pagina = request.POST.get('input_pagina', None)

        if not input_pagina:
            if form.is_valid():
                dados = form.cleaned_data
                novo_cliente = Cliente.objects.create(
                    nome=dados['nome'],
                    numHab=dados['numHab'],
                    endereco=dados['endereco'],
                    telefone=dados['telefone'])
                novo_cliente.save()
                return JsonResponse({'cliente': f'{novo_cliente}'})
            else:
                raise Http404
        else:
            return redirect('listaClientes')


class ListarClientesView(LoginRequiredMixin, ListView):
    template_name = 'servicos/clientes/listaCliente.html'
    model = Cliente
    context_object_name = 'clientes'


class EditarClienteView(LoginRequiredMixin, UpdateView):
    template_name = 'servicos/clientes/editarCliente.html'
    model = Cliente
    fields = ['nome', 'numHab', 'endereco', 'telefone']
    context_object_name = 'cliente'
    success_url = reverse_lazy('listaClientes')


class RemoverClienteView(LoginRequiredMixin, DeleteView):
    template_name = 'servicos/clientes/excluirCliente.html'
    model = Cliente
    success_url = reverse_lazy('listaClientes')
