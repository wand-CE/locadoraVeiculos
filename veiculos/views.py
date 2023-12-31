from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import TemplateView, ListView, FormView, CreateView, DeleteView, UpdateView
from django.contrib import messages
from veiculos.forms import CriarContratoForm, CriarClienteForm, OnibusForm, AutomovelForm
from veiculos.models import Veiculo, TipoVeiculo, Contrato, Cliente, Automovel, Onibus
from django.contrib.auth.models import User


class HomeView(ListView):
    template_name = 'index.html'
    queryset = TipoVeiculo.tipoquery.all()
    context_object_name = 'cars'


class LoginUserView(FormView):
    template_name = 'usuario/login.html'
    model = User
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        redirect_to = self.request.GET.get('next', '')
        if url_has_allowed_host_and_scheme(redirect_to, allowed_hosts=self.request.get_host()):
            return redirect_to
        return super().get_success_url()

    def form_valid(self, form):
        username = form.cleaned_data['username']
        senha = form.cleaned_data['password']

        usuario = authenticate(self.request, username=username, password=senha)
        if usuario is not None:
            login(self.request, usuario)
            messages.success(self.request, f'Seja bem vindo {username}!')
            return redirect(self.get_success_url())

        return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível logar')
        return redirect('loginusuario')


class LogoutUserView(LoginRequiredMixin, LogoutView):

    def get(self, request):
        logout(request)
        return redirect('home')


class ListaContratoView(LoginRequiredMixin, ListView):
    template_name = 'servicos/contratos/listaContratos.html'
    model = Contrato
    queryset = Contrato.objects.all()
    context_object_name = 'contratos'


class CriarContratoView(LoginRequiredMixin, CreateView):
    template_name = 'servicos/contratos/criarContrato.html'
    success_url = reverse_lazy('listaContratos')

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user

        if user.groups.filter(name='especiais').exists():
            return super().dispatch(request, *args, **kwargs)

        messages.error(self.request,
                       'Você não faz parte do grupo especiais para manipular contratos, peça para seu admin colocá-lo')
        return redirect('listaContratos')

    def get_form_class(self):
        hoje = datetime.now().date()

        for veiculo in Veiculo.objects.filter(disponivel=False):
            contratos = Contrato.objects.filter(veiculo=veiculo)
            if contratos:
                contrato_recente = contratos.order_by('-duracao').first()
                if contrato_recente.duracao < hoje:
                    veiculo.disponivel = True
                    veiculo.save()
            else:
                veiculo.disponivel = True
                veiculo.save()
        return CriarContratoForm

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data()
        contexto['form_criar_cliente'] = CriarClienteForm
        return contexto

    def form_valid(self, form):
        form.save()
        messages.success(self.request, message='Contrato cadastrado!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, message='Contrato não cadastrado')
        return super().form_invalid(form)


class RemoverContratoView(LoginRequiredMixin, DeleteView):
    model = Contrato
    template_name = 'servicos/contratos/removerContrato.html'
    success_url = reverse_lazy('listaContratos')

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user

        if user.groups.filter(name='especiais').exists():
            return super().dispatch(request, *args, **kwargs)

        messages.error(self.request,
                       'Você não faz parte do grupo especiais para manipular contratos, peça para seu admin colocá-lo')
        return redirect('listaContratos')


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


class ListarVeiculoView(ListView):
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
    template_name = 'servicos/veiculos/editarVeiculo.html'
    success_url = reverse_lazy('listaVeiculos')
    model = TipoVeiculo

    def get_form_class(self):
        form_type = self.kwargs.get('tipoVeiculo', None)

        if form_type == 'Automóvel':
            return AutomovelForm
        elif form_type == 'Ônibus':
            return OnibusForm

        raise Http404


class CriarClienteView(LoginRequiredMixin, FormView):
    template_name = 'servicos/clientes/criarCliente.html'
    form_class = CriarClienteForm

    def post(self, request, *args, **kwargs):
        form = CriarClienteForm(request.POST)
        input_pagina = request.POST.get('input_pagina', None)

        if form.is_valid():
            dados = form.cleaned_data
            novo_cliente = Cliente.objects.create(
                nome=dados['nome'],
                numHab=dados['numHab'],
                endereco=dados['endereco'],
                telefone=dados['telefone'])
            novo_cliente.save()

            if not input_pagina:
                return JsonResponse({'nome': f'{novo_cliente}', 'cliente_id': novo_cliente.id})
            else:
                messages.success(self.request, message='Cliente Cadastrado!!!')
                return redirect('listaClientes')
        else:
            if not input_pagina:
                return JsonResponse({'erro': 'erro ao criar novo Cliente'})
            else:
                return render(request, self.template_name, {'form': form, })


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
