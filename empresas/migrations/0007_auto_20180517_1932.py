# Generated by Django 2.0.4 on 2018-05-17 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0006_auto_20180513_0541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empresa',
            name='empresas',
        ),
        migrations.RemoveField(
            model_name='estrangeiro',
            name='empresas',
        ),
        migrations.RemoveField(
            model_name='pessoafisica',
            name='empresas',
        ),
    ]
