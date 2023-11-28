# Generated by Django 4.2.5 on 2023-11-27 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('veiculos', '0003_alter_automovel_managers_alter_onibus_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='veiculos.cliente'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='numEscritorio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='veiculos.escritorio'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='veiculo',
            field=models.ForeignKey(limit_choices_to={'disponivel': True}, null=True,
                                    on_delete=django.db.models.deletion.SET_NULL, to='veiculos.veiculo'),
        ),
    ]