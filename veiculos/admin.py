from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from veiculos.forms import VeiculoForm, AutomovelForm, OnibusForm
from veiculos.models import Cliente, Veiculo, Onibus, Automovel, Contrato, Escritorio, TipoVeiculo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'numHab', 'telefone']


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'placa']

    def nome(self, instance):
        try:
            return instance.tipoVeiculo
        except ObjectDoesNotExist:
            return 'ERROR!!'


@admin.register(Onibus)
class OnibusAdmin(admin.ModelAdmin):
    form = OnibusForm
    list_display = ['nome', 'numPassageiros',
                    'placa', 'dataProxManut', 'disponivel']

    def get_veiculo(self, instance, attribute):
        try:
            veiculo = Veiculo.objects.get(tipoVeiculo=instance)
            return getattr(veiculo, attribute)
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def placa(self, instance):
        return self.get_veiculo(instance, 'placa')

    def disponivel(self, instance):
        return self.get_veiculo(instance, 'disponivel')

    disponivel.boolean = True

    def dataProxManut(self, instance):
        return self.get_veiculo(instance, 'dataProxManut')

    dataProxManut.short_description = 'Data da próxima manutenção'


@admin.register(Automovel)
class AutomovelAdmin(admin.ModelAdmin):
    form = AutomovelForm

    list_display = ['nome', 'numPortas',
                    'placa', 'dataProxManut', 'disponivel']

    def get_veiculo(self, instance, attribute):
        try:
            veiculo = Veiculo.objects.get(tipoVeiculo=instance)
            return getattr(veiculo, attribute)
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def placa(self, instance):
        return self.get_veiculo(instance, 'placa')

    def disponivel(self, instance):
        return self.get_veiculo(instance, 'disponivel')

    disponivel.boolean = True

    def dataProxManut(self, instance):
        return self.get_veiculo(instance, 'dataProxManut')

    dataProxManut.short_description = 'Data da próxima manutenção'


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ['escritorio', 'cliente', 'veiculo', 'data', 'duracao']

    def escritorio(self, instance):
        try:
            return Escritorio.objects.get(id=instance.numEscritorio.id)
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def cliente(self, instance):
        try:
            return Cliente.objects.get(id=instance.cliente.id)
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def veiculo(self, instance):
        try:
            return Veiculo.objects.get(id=instance.veiculo.id)
        except ObjectDoesNotExist:
            return 'ERROR!!'

    def dataProxManut(self, instance):
        return self.get_veiculo(instance, 'dataProxManut')

    dataProxManut.short_description = 'Data da próxima manutenção'


@admin.register(Escritorio)
class EscritorioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'local']
