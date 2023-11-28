from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from stdimage import StdImageField


class Escritorio(models.Model):
    nome = models.CharField(max_length=250, unique=True, null=False)
    local = models.CharField(max_length=250, null=False)

    class Meta:
        verbose_name = 'Escritório'
        verbose_name_plural = 'Escritórios'

    def __str__(self):
        return f'Escritório: {self.nome}'


class Cliente(models.Model):
    nome = models.CharField(max_length=100, null=False)
    numHab = models.CharField(max_length=11, null=False, verbose_name="Número de Habilitação")
    endereco = models.CharField(max_length=250, null=False)
    telefone = models.CharField(max_length=11, null=False)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f'Cliente: {self.nome}'


class TipoVeiculoDisp(models.Manager):

    def get_queryset(self):
        return super().get_queryset()


class TipoVeiculo(models.Model):
    tipoquery = TipoVeiculoDisp()
    nome = models.CharField(max_length=100, null=False, verbose_name="Nome do veiculo")
    arCond = models.BooleanField(default=False, verbose_name="Ar-condicionado")
    foto = StdImageField(upload_to='car_photos', default='car_photos/no_car.png', verbose_name='Foto Carro')

    def __str__(self):
        return f'Veículo: {self.nome}'


class Automovel(TipoVeiculo):
    numPortas = models.IntegerField(choices=[(2, '2 portas'), (4, '4 portas')], null=False,
                                    verbose_name="Número de Portas", default=4)
    dirHidraulica = models.BooleanField(default=False, null=False, verbose_name="Direção Hidráulica")
    cambioAuto = models.BooleanField(default=False, null=False, verbose_name="Cambio Automático")

    class Meta:
        verbose_name = 'Automovel'
        verbose_name_plural = 'Automóveis'

    def __str__(self):
        return f'Automóvel: {self.nome}'


class Onibus(TipoVeiculo):
    numPassageiros = models.IntegerField(validators=[MaxValueValidator(104), MinValueValidator(32)], null=False,
                                         default=32, verbose_name='Número de Passageiros')
    leito = models.BooleanField(default=False, null=False)
    sanitario = models.BooleanField(default=False, null=False)

    class Meta:
        verbose_name = 'Onibus'
        verbose_name_plural = 'Onibus'

    def __str__(self):
        return f'Onibus: {self.nome}'


class Veiculo(models.Model):
    tipoVeiculo = models.OneToOneField(TipoVeiculo, on_delete=models.CASCADE, verbose_name='Veiculo')
    dataProxManut = models.DateField(null=False, verbose_name="Data da próxima Manutenção")
    placa = models.CharField(max_length=7, null=False, unique=True)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.tipoVeiculo.__str__()

    def mudar_disponivel(self):
        self.disponivel = False
        self.save()


class Contrato(models.Model):
    numEscritorio = models.ForeignKey(Escritorio, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True, limit_choices_to={'disponivel': True})
    data = models.DateField(auto_now_add=True, null=False)
    duracao = models.IntegerField(null=False, verbose_name='Duração do Contrato em dias')

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
