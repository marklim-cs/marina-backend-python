# Generated by Django 4.2.10 on 2024-02-15 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_student_date_of_birth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='countries_to_go',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]