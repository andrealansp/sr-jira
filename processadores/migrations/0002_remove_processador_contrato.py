# Generated by Django 5.2.2 on 2025-06-07 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processadores', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processador',
            name='contrato',
        ),
    ]
