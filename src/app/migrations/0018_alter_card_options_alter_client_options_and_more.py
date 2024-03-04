# Generated by Django 4.2.10 on 2024-03-01 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_client_balance_client_account_balance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={},
        ),
        migrations.RemoveField(
            model_name='client',
            name='account_balance',
        ),
        migrations.RemoveField(
            model_name='client',
            name='account_number',
        ),
        migrations.AddField(
            model_name='card',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.client'),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.client')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.account'),
        ),
    ]
