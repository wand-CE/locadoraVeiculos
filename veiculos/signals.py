from django.db.models.signals import post_save
from django.dispatch import receiver

from veiculos.models import Contrato


@receiver(post_save, sender=Contrato)
def mudar_disponivel(sender, instance, created, **kwargs):
    veiculo = instance.veiculo
    if veiculo:
        veiculo.disponivel = False
        veiculo.save()
