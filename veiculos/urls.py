from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cadastrousuario/', views.CadUsuarioView.as_view(), name='cadusuario'),
    path('loginusuario/', views.LoginUserView.as_view(), name='loginusuario'),
    path('logoutinusuario/', views.LogoutUserView.as_view(), name='logoutusuario'),
    path('criarContrato/', views.CriarContratoView.as_view(), name='criarContrato'),
    path('criarCliente/', views.CriarClienteView.as_view(), name='criarCliente'),
]
