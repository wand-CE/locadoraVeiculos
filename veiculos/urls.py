from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/login/', views.LoginUserView.as_view(), name='loginusuario'),
    path('logoutusuario/', views.LogoutUserView.as_view(), name='logoutusuario'),

    path('criarContrato/', views.CriarContratoView.as_view(), name='criarContrato'),
    path('listaContratos/', views.ListaContratoView.as_view(), name='listaContratos'),
    path('removerContrato/<pk>', views.RemoverContratoView.as_view(), name='removerContrato'),

    path('criarCliente/', views.CriarClienteView.as_view(), name='criarCliente'),
    path('listarClientes/', views.ListarClientesView.as_view(), name='listaClientes'),
    path('editarCliente/<int:pk>', views.EditarClienteView.as_view(), name='editarCliente'),
    path('removerCliente/<pk>', views.RemoverClienteView.as_view(), name='removerCliente'),

    path('criarVeiculo/', views.CriarVeiculoView.as_view(), name='criarVeiculo'),
    path('listaVeiculos/', views.ListarVeiculoView.as_view(), name='listaVeiculos'),
    path('editarVeiculo/<int:pk>/<str:tipoVeiculo>', views.EditarVeiculoView.as_view(), name='editarVeiculo'),
    path('removerVeiculo/<pk>', views.RemoverVeiculoView.as_view(), name='removerVeiculo'),
]
