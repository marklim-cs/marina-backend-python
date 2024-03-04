# Generated by Django 4.2.10 on 2024-03-01 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_card_account_card_balance_delete_account'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
        migrations.RemoveField(
            model_name='card',
            name='client',
        ),
        migrations.AddField(
            model_name='client',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.card'),
        ),
    ]