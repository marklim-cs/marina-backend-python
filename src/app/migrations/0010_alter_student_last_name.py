# Generated by Django 4.2.10 on 2024-02-10 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_student_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
